import csv

from src.config import settings


def read_video_ids_from_csv(csv_path: str) -> list[str]:
  print("STEP1:CSV読み込み")
  with open(csv_path, newline="", encoding=settings.ENCODING) as f:
    return [row[0] for row in csv.reader(f) if row]


def get_adopted_video_ids_from_score(score_csv_path: str) -> list[str]:
  """movie_score CSVから評価結果が「採用」の動画IDのみを返す。"""
  adopted = []
  with open(score_csv_path, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)  # ヘッダースキップ
    for row in reader:
      if len(row) >= 7 and row[6].strip() == "採用":
        adopted.append(row[0].strip())
  return adopted


def remove_video_id_from_csv(csv_path: str, video_id: str) -> None:
  with open(csv_path, newline="", encoding=settings.ENCODING) as f:
    rows = [row for row in csv.reader(f) if row and row[0] != video_id]
  with open(csv_path, "w", newline="", encoding=settings.ENCODING) as f:
    csv.writer(f).writerows(rows)
