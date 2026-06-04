import csv

from src.config import settings


def read_video_ids_from_csv(csv_path: str) -> list[str]:
  print("STEP1:CSV読み込み")
  with open(csv_path, newline="", encoding=settings.ENCODING) as f:
    return [row[0] for row in csv.reader(f) if row]


def remove_video_id_from_csv(csv_path: str, video_id: str) -> None:
  with open(csv_path, newline="", encoding=settings.ENCODING) as f:
    rows = [row for row in csv.reader(f) if row and row[0] != video_id]
  with open(csv_path, "w", newline="", encoding=settings.ENCODING) as f:
    csv.writer(f).writerows(rows)
