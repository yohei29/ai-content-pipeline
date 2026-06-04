
import os
# from googleapiclient.discovery import build
from google import genai

from src.config import constants
from src.config import settings

# custom utils
from src.utils.work_paths import WorkPaths
from src.utils.csv_utils import get_adopted_video_ids_from_score

# init
from pathlib import Path
raw_metadata_dir = Path(f"{constants.AI_AUDIO_TRANSCRIPTS_TEXT_DIR}")
raw_metadata_dir.mkdir(parents=True, exist_ok=True)
raw_metadata_dir = Path(f"{constants.AI_RESPONSE_DIR}")
raw_metadata_dir.mkdir(parents=True, exist_ok=True)

# === GeminiAI設定 ===
client = genai.Client(api_key=constants.STEP1_GEMINI_API_KEY)
print(constants.STEP1_GEMINI_API_KEY)
def main():

  youtube_ids = get_adopted_video_ids_from_score(WorkPaths.get_movie_score_output_path())

  for youtube_id in youtube_ids:
    try:
      # プロンプト取得
      with open(WorkPaths.get_prompts_step_prompt_file_path(constants.STEP1_WORK_DIR), "r", encoding="utf-8") as f:
        base_context = f.read()
      if base_context is None:
        raise RuntimeError("base_context is empty")

      # 音声抽出テキスト情報取得
      with open(WorkPaths.get_audio_transcripts_text_path(youtube_id), "rb") as f:
        audio_extracting_data = f.read().decode("utf-8")
      if audio_extracting_data is None:
        raise RuntimeError("audio_extracting_data is empty")

      # AI実行
      print(f"AI exac")
      print(youtube_id)
      context = (
        base_context
        + f"【投入データ】\n\n"
        # + f"動画タイトル:{movie_info.MOVIE_TITLE}\n\n"
        # + f"動画URL:{movie_info.MOVIE_URL}\n\n"
        + f"【一次ソース：生の文字起こしテキスト】\n\n{audio_extracting_data}\n\n"
        + f"【最終指示】\n\n上記の【一次ソース：生の文字起こしテキスト】のみを絶対的な事実としてロックし、他の一切の先入観を排除してください。このデータに基づき、マスターガイドラインのルール（ことわざのラベル化禁止、三人称客観視点の徹底、出力途切れ禁止）を完璧に守った「STEP1：ISRレポート」をフルサイズで出力してください。\n\n"
        + f"投入データ、生の文字起こしテキストにて情報と不足している場合には、何が不足しているかのみを返却してください"
      )
      response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
      )

      print(f"AI resposen output")
      with open(WorkPaths.get_prompts_step_ai_response_file_path(youtube_id, constants.STEP1_AI_RESPONSE_FILE), "w", encoding="utf-8") as f:
        f.write(response.text.strip())

      print(f"success")
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
  print('START')

  main()

  print('END')