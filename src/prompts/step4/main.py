
import os
import csv
# from googleapiclient.discovery import build
from google import genai
from google.genai import types
import constants
from movie import movie_info
import json


# === GeminiAI設定 ===
client = genai.Client(api_key=constants.STEP4_GEMINI_API_KEY)

_STEP2_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP2_AI_RESPONSE_FILE)
_STEP3_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP3_AI_RESPONSE_FILE)


def is_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def main():
  try:
    # コンテキスト取得
    print ('')
    with open(WorkPaths.get_prompts_step_prompt_file_path(constants.STEP4_WORK_DIR), "r", encoding="utf-8") as f:
      context = f.read()

    # コンテキスト成形
    with open(_STEP2_AI_RESPONSE_FILE_PATH, "rb") as f:
      step2_ai_response_data = f.read()
    if step2_ai_response_data is None:
      raise RuntimeError("Gemini response is empty")
    if not is_json(step2_ai_response_data):
      raise ValueError("Gemini response is not JSON")

    with open(_STEP3_AI_RESPONSE_FILE_PATH, "rb") as f:
      step3_ai_response_data = f.read()
    if step3_ai_response_data is None:
      raise RuntimeError("Gemini response is empty")
    if not is_json(step3_ai_response_data):
      raise ValueError("Gemini response is not JSON")

    context = (
      f"{context}\n\n"
      + f"【投入データフォーマット】\n\nSTEP4を実行する際は、上記のガイドラインの下に、以下のフォーマットでデータをすべて合体させて送信してください。\n\n"
      + f"【投入データ】\n\n"
      + f"動画タイトル:{movie_info.MOVIE_TITLE}\n\n"
      + f"動画URL:{movie_info.MOVIE_URL}\n\n"
      + f"【STEP2：構造化データ（JSON）】\n\n{step2_ai_response_data}\n\n"
      + f"【STEP3：ファクトチェック＆クレンジング済みコンテキスト】\n\n{step3_ai_response_data}\n\n"
      + '【【最終指示】上記の【STEP3：クレンジング済みコンテキスト】および【STEP2（JSON）】のみを絶対的な事実としてロックし、他の一切の先入観を排除してください。このデータに基づき、ことわざの自然な融合、三人称客観視点の徹底、演出用HTMLクラスの適切な配置、そのまま動くミニゲーム（JavaScript）の組み込み、および出力途切れ禁止を完璧に守った「STEP4：完成版Web記事（HTMLコードブロックのみ）」をフルサイズで出力してください。'
    )

    # AI実行
    print(f"AI exac")
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=context,
      # config=types.GenerateContentConfig(
      #   max_output_tokens=constants.MAX_OUTPUT_TOKENS,           # 出力上限拡張
      # )
    )

    print(f"AI resposen output")
    with open(WorkPaths.get_prompts_step_ai_response_file_path(youtube_id, constants.STEP4_AI_RESPONSE_FILE), "w", encoding="utf-8") as f:
      f.write(response.text.strip())

    print(f"success")
  except Exception as e:
    print(f"error: {e}")

if __name__ == "__main__":
  print('START')

  main()

  print('END')