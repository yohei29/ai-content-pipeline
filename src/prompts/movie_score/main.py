
import csv
from google import genai
from pathlib import Path

from src.config import constants
from src.config import settings
from src.utils.work_paths import WorkPaths

Path(constants.MOVIE_SCORE_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(constants.ARCHIVE_MOVIE_SCORE_DIR).mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=constants.MOVIE_SCORE_GEMINI_API_KEY)

CSV_HEADER = "動画ID,学術・心理的実用性,合理性・教訓的価値,哲学的客観性,ゴシップ・娯楽ノイズ,総合推奨度スコア,評価結果,理由・分析"


def extract_data_row(response_text: str) -> str:
    """AIレスポンスからデータ行（スコア行）のみを抽出する。ヘッダー行は除外。"""
    lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    # ヘッダー行（数字で始まらない行）をスキップして最後のデータ行を返す
    for line in reversed(lines):
        if line and (line[0].isdigit() or line.startswith('"')):
            return line
    # フォールバック：最終行を返す
    return lines[-1] if lines else ""


def main():
    with open(WorkPaths.get_movie_ids_file_path(), newline='', encoding=settings.ENCODING) as f:
        reader = csv.reader(f)
        youtube_ids = [row[0] for row in reader if row]

    output_path = WorkPaths.get_movie_score_output_path()
    rejected_path = WorkPaths.get_movie_score_rejected_output_path()

    # ヘッダー行を書き込む（上書き）
    for path in (output_path, rejected_path):
        with open(path, "w", encoding="utf-8", newline='') as f:
            f.write(CSV_HEADER + "\n")

    with open(WorkPaths.get_movie_score_prompt_file_path(), "r", encoding="utf-8") as f:
        base_prompt = f.read()

    for youtube_id in youtube_ids:
        try:
            transcript_path = WorkPaths.get_audio_transcripts_text_path(youtube_id)
            with open(transcript_path, "rb") as f:
                transcript_text = f.read().decode("utf-8")

            context = base_prompt + f"\n\n【入力テキスト】\n\n{transcript_text}"

            print(f"AI実行中: {youtube_id}")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=context
            )

            data_row = extract_data_row(response.text.strip())
            row_with_id = f"{youtube_id},{data_row}"

            parsed = next(csv.reader([row_with_id]))
            is_adopted = len(parsed) > 6 and parsed[6].strip() == "採用"
            dest_path = output_path if is_adopted else rejected_path
            with open(dest_path, "a", encoding="utf-8", newline='') as f:
                f.write(row_with_id + "\n")

            archive_path = WorkPaths.get_archive_movie_score_path()
            archive_needs_header = not Path(archive_path).exists() or Path(archive_path).stat().st_size == 0
            with open(archive_path, "a", encoding="utf-8", newline='') as f:
                if archive_needs_header:
                    f.write(CSV_HEADER + "\n")
                f.write(row_with_id + "\n")

            print(f"success: {youtube_id}")
        except FileNotFoundError:
            print(f"transcript not found: {youtube_id}")
        except Exception as e:
            print(f"error [{youtube_id}]: {e}")


if __name__ == "__main__":
    print('START')
    main()
    print('END')
