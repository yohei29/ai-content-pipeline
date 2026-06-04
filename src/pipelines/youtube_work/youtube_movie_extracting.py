# Python 3.12 on Windows: register NVIDIA DLL path before importing torch/whisper.
import os
import sys

_dll_path = os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cublas", "bin")
if os.path.exists(_dll_path):
  os.add_dll_directory(_dll_path)

import shutil
import subprocess
import time
import traceback
from datetime import datetime
from pathlib import Path

import torch
import whisper

from src.config import constants, settings
from src.utils.csv_utils import read_video_ids_from_csv, remove_video_id_from_csv
from src.utils.work_paths import WorkPaths

LOG_DIR = Path(constants.LOGS_DIR) / "youtube_work"
TRANSCRIPTS_DIR = Path(constants.AI_AUDIO_TRANSCRIPTS_TEXT_DIR)
ARCHIVE_MOVIE_DIR = Path(constants.ARCHIVE_MOVIE_DIR)
ARCHIVE_WAV_DIR = Path(constants.ARCHIVE_WAV_DIR)
RAW_AUDIO_DIR = Path(constants.RAW_AUDIO_DIR)
WHISPER_MODEL_NAME = "medium"


def _ensure_dirs() -> None:
  for directory in (TRANSCRIPTS_DIR, ARCHIVE_MOVIE_DIR, ARCHIVE_WAV_DIR, RAW_AUDIO_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def _resolve_device() -> str:
  return "cuda" if torch.cuda.is_available() else "cpu"


def _log_device(model: whisper.Whisper) -> None:
  print("\n--- [デバイス接続チェック] -------------------------")
  if str(model.device).startswith("cuda"):
    gpu_name = torch.cuda.get_device_name(0)
    print(f" ✅ 使用デバイス: GPU (CUDA駆動) -> {gpu_name}")
    print(" 🚀 グラフィックボードを使用した高速処理を実行します。")
  else:
    print(" ⚠️ 使用デバイス: CPU")
    print(" 🐌 GPUが認識されなかったため、低速なCPUモードで処理します。")
  print("---------------------------------------------------\n")


def _format_elapsed(seconds: float) -> str:
  if seconds > 60:
    return f"{int(seconds // 60)}分 {seconds % 60:.2f}秒 ({seconds:.2f}秒)"
  return f"{seconds:.2f}秒"


def convert_to_wav(mp4_path: Path, wav_path: Path) -> None:
  if not mp4_path.is_file():
    raise FileNotFoundError(f"入力mp4ファイルなし: {mp4_path}")

  command = [
    "ffmpeg",
    "-i", str(mp4_path),
    "-y",
    "-vn",
    "-acodec", "pcm_s16le",
    "-ar", "16000",
    "-ac", "1",
    str(wav_path),
  ]
  subprocess.run(command, check=True, capture_output=True, text=True)


def _write_transcript(youtube_id: str, segments: list[dict]) -> tuple[Path, int]:
  output_path = Path(WorkPaths.get_audio_transcripts_text_path(youtube_id))
  total_chars = 0
  with output_path.open("w", encoding="utf-8") as f:
    for seg in segments:
      text = seg["text"].strip()
      total_chars += len(text)
      f.write(f"{text}\n")
  return output_path, total_chars


def _archive_media(youtube_id: str, mp4_path: Path, wav_path: Path) -> None:
  shutil.move(mp4_path, WorkPaths.put_archive_movie_path(youtube_id))
  shutil.move(wav_path, WorkPaths.put_archive_wav_path(youtube_id))


def _process_video(youtube_id: str, model: whisper.Whisper) -> dict:
  mp4_path = Path(WorkPaths.get_movie_data_file_path(youtube_id))
  wav_path = Path(WorkPaths.get_audio_data_file_path(youtube_id))
  print(f"\n処理対象: {youtube_id} / {mp4_path} / {wav_path}")

  convert_to_wav(mp4_path, wav_path)

  if not wav_path.is_file():
    raise FileNotFoundError(f"音声ファイルなし: {wav_path}")

  print("音声ファイル読み込み開始")
  start_time = time.time()
  print("音声ファイルあり: 文字起こし（transcribe）を開始します...")
  result = model.transcribe(str(wav_path), language="ja", fp16=False)
  elapsed_time = time.time() - start_time
  segments = result.get("segments", [])

  print("音声ファイル書き込み開始")
  output_path, total_chars = _write_transcript(youtube_id, segments)
  _archive_media(youtube_id, mp4_path, wav_path)

  print("\n--- [STEP 2 完了ログ] -----------------------------")
  print(f"動画ID : {youtube_id}")
  print(f"ファイル : {output_path}")
  print(f"抽出文字数 : {total_chars:,} 文字")
  print(f"かかった時間: {_format_elapsed(elapsed_time)}")
  print("---------------------------------------------------\n")

  return {
    "id": youtube_id,
    "output_path": str(output_path),
    "total_chars": total_chars,
    "elapsed_time": elapsed_time,
  }


def _format_error(e: BaseException) -> str:
  return f"{type(e).__name__}: {e}"


def _append_failure_to_log(log_path: Path, item: dict) -> None:
  lines = [f"失敗: {item['id']}", f"  エラー: {item['error']}"]
  if item.get("traceback"):
    lines.append("  トレースバック:")
    for tb_line in item["traceback"].splitlines():
      lines.append(f"    {tb_line}")
  with log_path.open("a", encoding=settings.ENCODING) as f:
    f.write("\n".join(lines) + "\n")


def _write_run_log(
  started_at: datetime,
  stats: dict,
  *,
  csv_path: str,
  device: str,
  log_path: Path,
) -> None:
  lines = [
    "=== youtube_movie_extracting 実行ログ ===",
    f"実行日時: {started_at.strftime('%Y-%m-%d %H:%M:%S')}",
    f"動画ID CSV: {csv_path}",
    f"Whisperモデル: {WHISPER_MODEL_NAME}",
    f"デバイス: {device}",
    "",
    "=== 処理サマリ ===",
    f"対象件数: {stats['total']}",
    f"  成功: {stats['succeeded']}",
    f"  失敗: {stats['failed']}",
    f"  スキップ: {stats['skipped']}",
  ]

  if stats["succeeded_items"]:
    lines.append("")
    lines.append("成功:")
    for item in stats["succeeded_items"]:
      lines.append(
        f"  - {item['id']}: {item['total_chars']:,}文字 "
        f"({_format_elapsed(item['elapsed_time'])}) -> {item['output_path']}"
      )

  if stats["failed_items"]:
    lines.append("")
    lines.append("失敗 (詳細は上記):")
    for item in stats["failed_items"]:
      lines.append(f"  - {item['id']}: {item['error']}")

  with log_path.open("a", encoding=settings.ENCODING) as f:
    f.write("\n".join(lines) + "\n")


def main() -> None:
  started_at = datetime.now()
  _ensure_dirs()

  device = _resolve_device()
  print("テキスト出力開始")
  csv_path = WorkPaths.get_movie_ids_file_path()
  youtube_ids = read_video_ids_from_csv(csv_path)

  model = whisper.load_model(WHISPER_MODEL_NAME, device=device)
  _log_device(model)

  log_path = LOG_DIR / f"youtube_movie_extracting_{started_at.strftime('%Y%m%d_%H%M%S')}.log"

  stats = {
    "total": len(youtube_ids),
    "succeeded": 0,
    "failed": 0,
    "skipped": 0,
    "succeeded_items": [],
    "failed_items": [],
  }

  for youtube_id in youtube_ids:
    transcript_path = Path(WorkPaths.get_audio_transcripts_text_path(youtube_id))
    if transcript_path.is_file():
      print(f"スキップ: {youtube_id} (トランスクリプト出力済み: {transcript_path})")
      stats["skipped"] += 1
      continue

    try:
      item = _process_video(youtube_id, model)
      stats["succeeded"] += 1
      stats["succeeded_items"].append(item)
      remove_video_id_from_csv(csv_path, youtube_id)
    except Exception as e:
      failed_item = {
        "id": youtube_id,
        "error": _format_error(e),
        "traceback": traceback.format_exc(),
      }
      stats["failed"] += 1
      stats["failed_items"].append(failed_item)
      _append_failure_to_log(log_path, failed_item)
      print("================================")
      print(f"処理失敗: {youtube_id}")
      print(e)
      print("================================")

  _write_run_log(started_at, stats, csv_path=csv_path, device=device, log_path=log_path)
  print(f"ログ保存: {log_path}")


if __name__ == "__main__":
  main()
