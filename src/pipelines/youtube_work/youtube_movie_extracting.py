# --------------------------------------------------
# パッチコード（Python 3.12のDLL探索バグを最優先で回避）
# --------------------------------------------------
import os
import sys
# 仮想環境（.venv_gpu312）の中にあるNVIDIAのDLLフォルダを直接登録して強制認識させます
dll_path = os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cublas", "bin")
if os.path.exists(dll_path):
    os.add_dll_directory(dll_path)

import whisper
import subprocess
import csv
import shutil
import torch
import time

from src.config import constants
from src.config import settings

# custom utils
from src.utils.work_paths import WorkPaths

# init
from pathlib import Path
raw_metadata_dir = Path(f"{constants.AI_AUDIO_TRANSCRIPTS_TEXT_DIR}")
raw_metadata_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# メイン
# --------------------------------------------------

def main():

  # local variable
  # 使用するデバイスの判定（GPUが使えればcuda、なければcpu）
  _device = "cuda" if torch.cuda.is_available() else "cpu"

  print("テキスト出力開始")
  youtube_ids = read_video_ids_from_csv(WorkPaths.get_movie_ids_file_path())

  for youtube_id in youtube_ids:
    input_mp4_file_path = WorkPaths.get_movie_data_file_path(youtube_id)
    input_wav_file_path = WorkPaths.get_audio_data_file_path(youtube_id)
    print(f"\n処理対象: {youtube_id} / {input_mp4_file_path} / {input_wav_file_path}")

    convert_to_wav(input_mp4_file_path, input_wav_file_path)

    print("音声ファイル読み込み開始")
    # モデルのロード時に device を明示的に指定
    model = whisper.load_model("medium", device=_device)
    # model = whisper.load_model("large", device=_device)

    # --- 【追加】GPU使用状況の確認とログ出力 ---
    print("\n--- [デバイス接続チェック] -------------------------")
    if str(model.device).startswith("cuda"):
      gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Unknown GPU"
      print(f" ✅ 使用デバイス: GPU (CUDA駆動) -> {gpu_name}")
      print(" 🚀 グラフィックボードを使用した高速処理を実行します。")
    else:
      print(" ⚠️ 使用デバイス: CPU")
      print(" 🐌 GPUが認識されなかったため、低速なCPUモードで処理します。")
    print("---------------------------------------------------\n")

    if os.path.isfile(input_wav_file_path):
      start_time = time.time()
      print("音声ファイルあり: 文字起こし（transcribe）を開始します...")
      # お使いのGPU環境（GTXシリーズ等）の制限を考慮し、fp16=False (32bit計算) で安全に実行
      result = model.transcribe(input_wav_file_path, language="ja", fp16=False)
      end_time = time.time()
      elapsed_time = end_time - start_time
      total_chars = sum(len(segment["text"]) for segment in result.get("segments", []))
    else:
      print("音声ファイルなし")
      exit()

    print("音声ファイル書き込み開始")
    youtube_audio_transcript_output_file_path = WorkPaths.get_audio_transcripts_text_path(youtube_id)
    with open(youtube_audio_transcript_output_file_path, "w", encoding="utf-8") as f:
      for i, seg in enumerate(result["segments"], start=1):
        f.write(f"{seg['text'].strip()}\n")

    shutil.move(
      input_mp4_file_path,
      WorkPaths.put_archive_movie_path(youtube_id)
    )
    shutil.move(
      input_wav_file_path,
      WorkPaths.put_archive_wav_path(youtube_id)
    )

    print("\n--- [STEP 2 完了ログ] -----------------------------")
    print(f"動画ID : {youtube_id}")
    print(f"ファイル : {youtube_audio_transcript_output_file_path}")
    print(f"抽出文字数 : {total_chars:,} 文字")
    if elapsed_time > 60:
      print(f"かかった時間: {int(elapsed_time // 60)}分 {elapsed_time % 60:.2f}秒 ({elapsed_time:.2f}秒)")
    else:
      print(f"かかった時間: {elapsed_time:.2f}秒")
    print("---------------------------------------------------\n")


def seconds_to_srt_time(seconds):
  hrs = int(seconds // 3600)
  mins = int((seconds % 3600) // 60)
  secs = int(seconds % 60)
  millis = int((seconds - int(seconds)) * 1000)
  return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

def convert_to_wav(input_mp4_file_path, input_wav_file_path):
  if not os.path.isfile(input_mp4_file_path):
    print("入力mp4ファイルなし:" + input_mp4_file_path)
    exit()

  command = [
    "ffmpeg",
    "-i", input_mp4_file_path,     # 入力ファイル
    "-y",                          # 上書き確認なし
    "-vn",                         # 映像無効（音声のみ）
    "-acodec", "pcm_s16le",        # リニアPCM 16bit
    "-ar", "16000",                # サンプリングレート 16kHz
    "-ac", "1",                    # モノラル
    input_wav_file_path
  ]
  result = subprocess.run(command, check=True, capture_output=True, text=True)

def read_video_ids_from_csv(csv_path):
  print ('STEP1:CSV読み込み')
  with open(csv_path, newline='', encoding=f'{settings.ENCODING}') as f:
    reader = csv.reader(f)
    return [row[0] for row in reader if row]

if __name__ == "__main__":
  main()
