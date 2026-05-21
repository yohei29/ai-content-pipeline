# --------------------------------------------------
# 動画ID一覧取得
# _channel_urlにある指定期間の動画IDを取得する。
# --------------------------------------------------

import os
import csv
import yt_dlp
from src.config import constants
from src.config import settings
from yt_dlp.utils import DateRange

# custom utils
from src.utils.work_paths import WorkPaths

# init
from pathlib import Path
raw_metadata_dir = Path(f"{constants.RAW_METADATA_DIR}")
raw_metadata_dir.mkdir(parents=True, exist_ok=True)
raw_metadata_movie_info_dir = Path(f"{constants.RAW_METADATA_DIR}")
raw_metadata_movie_info_dir.mkdir(parents=True, exist_ok=True)
movie_ids_file_path = WorkPaths.get_movie_ids_file_path()
Path(movie_ids_file_path).write_text("", encoding="utf-8")

# local variable
_channel_url = "https://www.youtube.com/@KanaeVCriminologist/streams"



# --------------------------------------------------
# メイン
# --------------------------------------------------

def main():
  entries = fetch_channel_video_list(_channel_url)

  results = []

  for entry in entries:

    video_id = entry.get("id")

    if not video_id:
        continue

    video_url = f"{constants.YOUTUBE_BASE_URL}{video_id}"

    try:
      detail = fetch_video_detail(video_url)
    except Exception as e:
      print("================================")
      print("取得失敗")
      print(video_url)
      print(e)
      print("================================")
      continue

    upload_date = detail.get("upload_date")

    if not is_target_date(upload_date):
        continue

    print(f"取得中: {video_id}")
    results.append(detail)

  print(f"取得件数: {len(results)}")
  save_video_infos(results)


# --------------------------------------------------
# 日付判定
# --------------------------------------------------

_date_from = "20260501"
_date_to   = "20260531"


def is_target_date(upload_date: str) -> bool:

  if upload_date is None:
    return False

  if _date_from and upload_date < _date_from:
    return False

  if _date_to and upload_date > _date_to:
    return False

  return True


# --------------------------------------------------
# チャンネル動画一覧取得
# --------------------------------------------------

def fetch_channel_video_list(channel_url: str):

  ydl_opts = {
    "extract_flat": True,
    "skip_download": True,
    "quiet": False,
    "daterange": DateRange(_date_from, _date_to),
    "playlistend": 5,  # 最初の5件だけを取得（1からカウント）
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    info = ydl.extract_info(
      f"{channel_url}/videos",
      download=False
    )

    return info.get("entries", [])


# --------------------------------------------------
# 動画詳細取得
# --------------------------------------------------

def fetch_video_detail(video_url: str):

    ydl_opts = {
      "skip_download": True,
      "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

      info = ydl.extract_info(
        video_url,
        download=False
      )

      return {
        "id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "upload_date": info.get("upload_date"),
        "webpage_url": info.get("webpage_url"),
      }


# --------------------------------------------------
# CSV保存
# 今後RDBチックにデータを蓄積させる時用に
# --------------------------------------------------

def save_csv_video_infos(video_infos, output_path):

  with open(output_path, "w", newline="", encoding=f"{settings.ENCODING}") as f:

    writer = csv.writer(f)

    # ヘッダ
    writer.writerow([
      "video_id",
      "title",
      "description",
      "upload_date",
      "url"
    ])

    for item in video_infos:
      writer.writerow([
        item["id"],
        item["title"],
        item["description"],
        item["upload_date"],
        item["webpage_url"]
      ])

    print(f"保存完了: {output_path}")


# --------------------------------------------------
# 動画情報保存
# --------------------------------------------------

def save_video_infos(video_infos):
  for item in video_infos:
    output_ids_path   = movie_ids_file_path
    output_info_path  = f"{constants.RAW_METADATA_MOVIE_INFO_DIR}{item["id"]}_{constants.MOVIE_INFO_FILE}"
    with open(output_ids_path, "a", newline="", encoding=f"{settings.ENCODING}") as f:
      f.write(f"{item['id']}\n")
    with open(output_info_path, "w", newline="", encoding=f"{settings.ENCODING}") as f:
      writer = csv.writer(f)
      writer.writerow([
          item["id"],
          item["title"],
          item["description"],
          item["upload_date"],
          item["webpage_url"]
      ])

    print(f"保存完了: {output_ids_path} / {output_info_path}")

if __name__ == "__main__":
  main()
