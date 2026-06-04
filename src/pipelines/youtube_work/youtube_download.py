import traceback
from datetime import datetime
from pathlib import Path

from src.utils.ssl_certs import configure_ssl_certs

configure_ssl_certs()

import yt_dlp

from src.config import constants, settings
from src.utils.csv_utils import read_video_ids_from_csv
from src.utils.work_paths import WorkPaths
from src.utils.yt_dlp_opts import merge_ydl_opts

RAW_VIDEOS_DIR = Path(constants.RAW_VIDEOS_DIR)
LOG_DIR = Path(constants.LOGS_DIR) / "youtube_work"


def _ensure_raw_videos_dir() -> None:
  RAW_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_log_dir() -> None:
  LOG_DIR.mkdir(parents=True, exist_ok=True)


def _is_already_downloaded(youtube_id: str) -> bool:
  return Path(WorkPaths.get_movie_data_file_path(youtube_id)).is_file()


def _download_video(youtube_id: str) -> None:
  video_url = f"{constants.YOUTUBE_BASE_URL}{youtube_id}"
  print(video_url)
  ydl_opts = merge_ydl_opts({
    "outtmpl": str(RAW_VIDEOS_DIR / f"{youtube_id}.%(ext)s"),
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
  })
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(video_url)


def _format_error(e: BaseException) -> str:
  return f"{type(e).__name__}: {e}"


def _write_run_log(
  started_at: datetime,
  stats: dict,
  *,
  csv_path: str,
) -> Path:
  log_path = LOG_DIR / f"youtube_download_{started_at.strftime('%Y%m%d_%H%M%S')}.log"
  lines = [
    "=== youtube_download 実行ログ ===",
    f"実行日時: {started_at.strftime('%Y-%m-%d %H:%M:%S')}",
    f"動画ID CSV: {csv_path}",
    "",
    "=== 処理サマリ ===",
    f"対象件数: {stats['total']}",
    f"  スキップ（既存）: {stats['already_downloaded']}",
    f"  ダウンロード成功: {stats['succeeded']}",
    f"  ダウンロード失敗: {stats['failed']}",
  ]

  if stats["failed_items"]:
    lines.append("")
    lines.append("ダウンロード失敗:")
    for item in stats["failed_items"]:
      lines.append(f"  - {item['id']}: {item['url']}")
      lines.append(f"    エラー: {item['error']}")
      if item.get("traceback"):
        lines.append("    トレースバック:")
        for tb_line in item["traceback"].splitlines():
          lines.append(f"      {tb_line}")

  log_path.write_text("\n".join(lines) + "\n", encoding=settings.ENCODING)
  return log_path


def main() -> None:
  started_at = datetime.now()
  _ensure_raw_videos_dir()
  _ensure_log_dir()

  csv_path = WorkPaths.get_movie_ids_file_path()
  youtube_ids = read_video_ids_from_csv(csv_path)
  stats = {
    "total": len(youtube_ids),
    "already_downloaded": 0,
    "succeeded": 0,
    "failed": 0,
    "failed_items": [],
  }

  for youtube_id in youtube_ids:
    if _is_already_downloaded(youtube_id):
      print(f"already movie : {youtube_id}")
      stats["already_downloaded"] += 1
      continue

    video_url = f"{constants.YOUTUBE_BASE_URL}{youtube_id}"
    try:
      _download_video(youtube_id)
      stats["succeeded"] += 1
    except Exception as e:
      stats["failed"] += 1
      stats["failed_items"].append({
        "id": youtube_id,
        "url": video_url,
        "error": _format_error(e),
        "traceback": traceback.format_exc(),
      })
      print("================================")
      print("ダウンロード失敗")
      print(video_url)
      print(e)
      print("================================")

  log_path = _write_run_log(started_at, stats, csv_path=csv_path)
  print(f"ログ保存: {log_path}")


if __name__ == "__main__":
  main()
