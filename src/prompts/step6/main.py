
import os
import csv
# from googleapiclient.discovery import build
from google import genai
from google.genai import types
import constants
from movie import movie_info
import json


# === GeminiAI設定 ===
client = genai.Client(api_key=constants.STEP6_GEMINI_API_KEY)

_YOUTUBE_AUDIO_TRANSCRIPT_OUTPUT_FILE_PATH = os.path.join(constants.YOUTUBE_AUDIO_TRANSCRIPT_OUTPUT_FILE, constants.YOUTUBE_AUDIO_TRANSCRIPT_OUTPUT_FILE)
_STEP2_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP2_AI_RESPONSE_FILE)
_STEP3_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP3_AI_RESPONSE_FILE)
_STEP4_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP4_AI_RESPONSE_FILE)
_STEP5_AI_RESPONSE_FILE_PATH = os.path.join(constants.AI_RESPONSE_DIR, constants.STEP5_AI_RESPONSE_FILE)

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
    with open(WorkPaths.get_prompts_step_prompt_file_path(constants.STEP6_WORK_DIR), "r", encoding="utf-8") as f:
      context = f.read()

    # コンテキスト成形
    with open(_STEP2_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step2_ai_response_data = f.read()
    if step2_ai_response_data is None:
      raise RuntimeError("step2_ai_response_data response is empty")
    if not is_json(step2_ai_response_data):
      raise ValueError("step2_ai_response_data response is not JSON")

    with open(_STEP3_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step3_ai_response_dict = json.load(f)
    if step3_ai_response_dict is None:
      raise RuntimeError("step3_ai_response_dict response is empty")

    with open(_STEP4_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step4_ai_response_data = f.read()
    if step4_ai_response_data is None:
      raise RuntimeError("step4_ai_response_data response is empty")

    with open(_STEP5_AI_RESPONSE_FILE_PATH, "r", encoding="utf-8") as f:
      step5_ai_response_data = f.read()
    if step5_ai_response_data is None:
      raise RuntimeError("step5_ai_response_data response is empty")

    context = (
      f"{context}\n\n"
      + f"【投入データフォーマット】\n\nSTEP6を実行する際は、上記のガイドラインの下に、以下のフォーマットでデータをすべて合体させて送信してください。\n\n"
      + f"【投入データ】\n\n"
      + f"【STEP2：構造化データ（JSON）】\n\n{step2_ai_response_data}\n\n"
      + f"【STEP3：ファクトチェック＆クレンジング済みコンテキスト】\n\n{step3_ai_response_dict["cleansed_context"]}\n\n"
      + f"【STEP4：修正前のHTML記事】\n\n{step4_ai_response_data}\n\n"
      + f"【STEP5：検品結果・修正指示（JSON）】\n\n{step5_ai_response_data}\n\n"
      + '【最終指示】【STEP5：検品結果・修正指示】を神の宣告として受け止め、指摘された不備やコード切れを完全に克服してください。【STEP2】および【STEP3】のマスターデータに完全ロックし、他の一切の先入観を排除します。三人称客観視点の徹底、ことわざのステルス融合、ミニゲームの完全コード化、そして出力途切れ禁止を完璧にクリアした「STEP6：完全化された最終HTML（```html コードブロックのみ）」をフルサイズで出力してください。'
    )

    # AI実行
    print(f"AI exac")
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=context,
      config=types.GenerateContentConfig(
        max_output_tokens=constants.MAX_OUTPUT_TOKENS,           # 出力上限拡張
      )
    )

    print(f"AI resposen output")
    with open(WorkPaths.get_prompts_step_ai_response_file_path(youtube_id, constants.STEP6_AI_RESPONSE_FILE), "w", encoding="utf-8") as f:
      f.write(response.text.strip())

    print(f"success")
  except Exception as e:
    print(f"error: {e}")

if __name__ == "__main__":
  print('START')

  main()

  print('END')