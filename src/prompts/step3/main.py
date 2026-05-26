
import os
import csv
# from googleapiclient.discovery import build
from google import genai
from google.genai import types
import constants
from movie import movie_info


# === GeminiAI設定 ===
client = genai.Client(api_key=constants.STEP3_GEMINI_API_KEY)

_STEP1_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP1_AI_RESPONSE_FILE)
_STEP2_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP2_AI_RESPONSE_FILE)

def main():
  try:
    # コンテキスト取得
    print ('')
    with open(WorkPaths.get_prompts_step_prompt_file_path(constants.STEP3_WORK_DIR), "r", encoding="utf-8") as f:
      context = f.read()

    # コンテキスト成形
    with open(_STEP1_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step1_ai_response_data = f.read()
    if step1_ai_response_data is None:
      raise RuntimeError("step1_ai_response_data is empty")

    with open(_STEP2_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step2_ai_response_data = f.read()
    if step2_ai_response_data is None:
      raise RuntimeError("step2_ai_response_data is empty")

    with open(WorkPaths.get_audio_transcripts_text_path(youtube_id), "r", encoding="utf-8") as f:
      audio_extracting_data = f.read()
    if audio_extracting_data is None:
      raise RuntimeError("audio_extracting_data is empty")

    context = (
      f"{context}\n\n"
      + f"### 基本情報\n\n"
      + f"動画タイトル:{movie_info.MOVIE_TITLE}\n\n"
      + f"動画URL:{movie_info.MOVIE_URL}\n\n"
      + f"【STEP1：解析レポート結果】\n\n{step1_ai_response_data}\n\n"
      + f"【STEP2：構造化データ（JSON）】\n\n{step2_ai_response_data}\n\n"
      + f"【一次ソース：生の文字起こしテキスト】\n\n{audio_extracting_data}\n\n"
      + '【最終指示】上記の【一次ソース：生の文字起こしテキスト】のみを絶対的な事実としてロックし、他の一切の先入観や別動画の記憶を排除してください。このデータに基づき、ノイズ定義・検証ルール・JSON出力フォーマット（出力途切れ禁止）を完璧に守った「STEP3：クレンジングレポート」をフルサイズで出力してください。'
    )

    # AI実行
    print(f"AI exac")
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=context,
      config=types.GenerateContentConfig(
        # max_output_tokens=constants.MAX_OUTPUT_TOKENS,           # 出力上限拡張
        response_mime_type="application/json" # 出力をJSONに固定
      )
    )

    print(f"AI resposen output")
    with open(WorkPaths.get_prompts_step_ai_response_file_path(youtube_id, constants.STEP3_AI_RESPONSE_FILE), "w", encoding="utf-8") as f:
      f.write(response.text.strip())

    print(f"success")
  except Exception as e:
    print(f"error: {e}")

if __name__ == "__main__":
  print('START')

  main()

  print('END')