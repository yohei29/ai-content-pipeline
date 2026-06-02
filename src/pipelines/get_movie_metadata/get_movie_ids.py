# --------------------------------------------------
# 動画ID一覧取得
# _channel_url がある指定期間の動画IDを取得する。
# python -m src.pipelines.get_movie_metadata.get_movie_ids
# --------------------------------------------------

import csv
from datetime import datetime
from pathlib import Path

from src.utils.ssl_certs import configure_ssl_certs

configure_ssl_certs()

import yt_dlp
from yt_dlp.utils import DateRange

from src.config import constants, settings
from src.utils.work_paths import WorkPaths
from src.utils.yt_dlp_opts import merge_ydl_opts

# --------------------------------------------------
# local constants（このファイル専用。constants.py とは別）
# --------------------------------------------------
_channel_url = "https://www.youtube.com/@KanaeVCriminologist/streams"
_date_from = "20260101"
_date_to = "20260430"
_get_max_movie_ids = 10


def main() -> None:
  setup_output_dirs()
  entries = fetch_channel_video_list(_channel_url, _date_from, _date_to, _get_max_movie_ids)
  video_infos, collect_stats = collect_video_infos(entries, _date_from, _date_to)
  log_run_summary(video_infos, collect_stats, playlist_entries=len(entries))
  save_video_infos(video_infos)


def setup_output_dirs() -> None:
  Path(constants.RAW_METADATA_DIR).mkdir(parents=True, exist_ok=True)
  Path(constants.RAW_METADATA_MOVIE_INFO_DIR).mkdir(parents=True, exist_ok=True)
  Path(constants.LOGS_DIR, "get_movie_metadata").mkdir(parents=True, exist_ok=True)
  Path(WorkPaths.get_movie_ids_file_path()).write_text("", encoding=settings.ENCODING)


def log_run_summary(
  video_infos: list[dict],
  collect_stats: dict,
  *,
  playlist_entries: int,
) -> None:
  now = datetime.now()
  log_dir = Path(constants.LOGS_DIR) / "get_movie_metadata"
  log_path = log_dir / f"get_movie_ids_{now.strftime('%Y%m%d_%H%M%S')}.log"
  count = len(video_infos)

  lines = [
    "=== get_movie_ids 実行ログ ===",
    f"実行日時: {now.strftime('%Y-%m-%d %H:%M:%S')}",
    f"チャンネルURL: {_channel_url}",
    f"取得URL: {_channel_url}/videos",
    f"期間: {_date_from} ～ {_date_to}",
    f"最大取得数: {_get_max_movie_ids}",
    "",
    "=== 処理サマリ ===",
    f"プレイリスト件数: {playlist_entries}",
    f"取得件数（期間内）: {count}",
    f"  詳細取得失敗: {collect_stats['fetch_failed']}",
    f"  期間外で除外: {collect_stats['date_filtered']}",
    f"  IDなしでスキップ: {collect_stats['no_id']}",
  ]

  if collect_stats["fetch_failed_items"]:
    lines.append("")
    lines.append("詳細取得失敗:")
    for item in collect_stats["fetch_failed_items"]:
      lines.append(f"  - {item['id']}: {item['error']}")

  if collect_stats["date_filtered_items"]:
    lines.append("")
    lines.append("期間外で除外（upload_date が指定期間外）:")
    for item in collect_stats["date_filtered_items"]:
      lines.append(f"  - {item['id']}: upload_date={item['upload_date']}")

  if count == 0 and playlist_entries > 0 and collect_stats["date_filtered"] > 0:
    lines.append("")
    lines.append(
      "※ プレイリストには動画がありますが、期間内の動画は0件です。"
      f" 直近の upload_date が {_date_to} より後の可能性があります。"
      " _date_to を延ばすか、期間を見直してください。"
    )

  if video_infos:
    lines.append("")
    lines.append("取得した動画:")
    for item in video_infos:
      lines.append(f"  - {item['id']}: {item.get('title', '')}")

  log_path.write_text("\n".join(lines) + "\n", encoding=settings.ENCODING)
  print(f"取得件数: {count}（プレイリスト: {playlist_entries}件）")
  if count == 0 and playlist_entries > 0:
    print(f"  → 期間外除外: {collect_stats['date_filtered']}件, 詳細取得失敗: {collect_stats['fetch_failed']}件")
  print(f"ログ保存: {log_path}")


def collect_video_infos(entries: list, date_from: str, date_to: str) -> tuple[list[dict], dict]:
  results = []
  stats = {
    "no_id": 0,
    "fetch_failed": 0,
    "date_filtered": 0,
    "fetch_failed_items": [],
    "date_filtered_items": [],
  }

  for entry in entries:
    video_id = entry.get("id")
    if not video_id:
      stats["no_id"] += 1
      continue

    video_url = f"{constants.YOUTUBE_BASE_URL}{video_id}"
    try:
      detail = fetch_video_detail(video_url)
    except Exception as e:
      stats["fetch_failed"] += 1
      stats["fetch_failed_items"].append({
        "id": video_id,
        "error": f"{type(e).__name__}: {e}",
      })
      print("================================")
      print("取得失敗")
      print(video_url)
      print(e)
      print("================================")
      continue

    upload_date = detail.get("upload_date")
    if not is_target_date(upload_date, date_from, date_to):
      stats["date_filtered"] += 1
      stats["date_filtered_items"].append({
        "id": video_id,
        "upload_date": upload_date,
      })
      continue

    print(f"取得中: {video_id}")
    results.append(detail)

  return results, stats


def is_target_date(upload_date: str | None, date_from: str, date_to: str) -> bool:
  if upload_date is None:
    return False
  if date_from and upload_date < date_from:
    return False
  if date_to and upload_date > date_to:
    return False
  return True


def fetch_channel_video_list(
  channel_url: str,
  date_from: str,
  date_to: str,
  max_count: int | None = None,
) -> list:
  ydl_opts = merge_ydl_opts({
    "extract_flat": True,
    "skip_download": True,
    "quiet": False,
    "daterange": DateRange(date_from, date_to),
  })
  if max_count:
    ydl_opts["playlistend"] = max_count

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(f"{channel_url}/videos", download=False)
    return info.get("entries", [])


def fetch_video_detail(video_url: str) -> dict:
  ydl_opts = merge_ydl_opts({
    "skip_download": True,
    "quiet": True,
  })
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)
    return {
      "id": info.get("id"),
      "title": info.get("title"),
      "description": info.get("description"),
      "upload_date": info.get("upload_date"),
      "webpage_url": info.get("webpage_url"),
    }


def save_video_infos(video_infos: list[dict]) -> None:
  ids_path = Path(WorkPaths.get_movie_ids_file_path())
  movie_info_dir = Path(constants.RAW_METADATA_MOVIE_INFO_DIR)

  with ids_path.open("a", encoding=settings.ENCODING) as ids_file:
    for item in video_infos:
      ids_file.write(f"{item['id']}\n")
      info_path = movie_info_dir / f"{item['id']}_{constants.MOVIE_INFO_FILE}"
      write_video_info_csv(item, info_path)
      print(f"保存完了: {ids_path} / {info_path}")


def write_video_info_csv(item: dict, output_path: Path) -> None:
  with output_path.open("w", newline="", encoding=settings.ENCODING) as f:
    writer = csv.writer(f)
    writer.writerow([
      item["id"],
      item["title"],
      item["description"],
      item["upload_date"],
      item["webpage_url"],
    ])


if __name__ == "__main__":
  main()
