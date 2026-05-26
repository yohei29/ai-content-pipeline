
import os
import yt_dlp
import csv
from src.config import constants
from src.config import settings

from pathlib import Path

# custom utils
from src.utils.work_paths import WorkPaths

# init
from pathlib import Path
raw_metadata_dir = Path(f"{constants.RAW_VIDEOS_DIR}")
raw_metadata_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# メイン
# --------------------------------------------------

def main():
  youtube_ids = read_video_ids_from_csv(WorkPaths.get_movie_ids_file_path())

  dl_file_names  = [p.name for p in Path(constants.RAW_VIDEOS_DIR).glob("*.mp4")]

  for youtube_id in youtube_ids:

    if any(youtube_id in file_name for file_name in dl_file_names):
      print(f"already movie : {youtube_id}")
      continue

    video_url = f"{constants.YOUTUBE_BASE_URL}{youtube_id}"
    print(video_url)
    # break
    ydl_opts = {
      'outtmpl': f'./{constants.RAW_VIDEOS_DIR}/{youtube_id}.%(ext)s',
      'format': 'bestvideo+bestaudio/best',
      'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download(video_url)

def read_video_ids_from_csv(csv_path):

  print ('STEP1:CSV読み込み')

  with open(csv_path, newline='', encoding=f"{settings.ENCODING}") as f:
    reader = csv.reader(f)
    return [row[0] for row in reader if row]

if __name__ == "__main__":
  main()
