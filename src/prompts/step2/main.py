
import os
import csv
# from googleapiclient.discovery import build
from google import genai
from google.genai import types
import constants
from movie import movie_info


# === GeminiAI設定 ===
client = genai.Client(api_key=constants.STEP2_GEMINI_API_KEY)

def main():
  try:
    # プロンプト取得
    print ('')
    with open(WorkPaths.get_prompts_step_prompt_file_path(constants.STEP2_WORK_DIR), "r", encoding="utf-8") as f:
      context = f.read()
    if context is None:
      raise RuntimeError("context is empty")

    # AI実行
    print(f"AI exac")
    with open(WorkPaths.get_audio_data_file_path(youtube_id), "rb") as f:
        audio_data = f.read()

    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[
        context,
        types.Part.from_bytes(
          data=audio_data,
          mime_type="audio/wav"
        )
      ],
      config=types.GenerateContentConfig(
        # max_output_tokens=constants.MAX_OUTPUT_TOKENS,           # 出力上限拡張
        response_mime_type="application/json" # 出力をJSONに固定
      )
    )

    print(f"AI resposen output")
    with open(WorkPaths.get_prompts_step_ai_response_file_path(youtube_id, constants.STEP2_AI_RESPONSE_FILE), "w", encoding="utf-8") as f:
      f.write(response.text.strip())

    print(f"success")
  except Exception as e:
      print(f"error: {e}")

if __name__ == "__main__":
  print('START')

  main()

  print('END')