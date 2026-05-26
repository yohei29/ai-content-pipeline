YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
NODE_PATH = "C:/Program Files/nodejs/node.exe"
MP4_EXTENSION = ".mp4"
WAV_EXTENSION = ".wav"

YOUTUBE_API_KEY = ''
GEMINI_API_KEY = ''
GEMINI_API_KEY_STEP2 = ''

# 動画メタデータ取得
## 動画ID一覧取得関連
RAW_METADATA_DIR = "./data/raw/metadata/"
RAW_METADATA_MOVIE_INFO_DIR = "./data/raw/metadata/movie_info_csv/"
MOVIE_IDS_FILE = "movie_ids.csv"
MOVIE_INFO_FILE = "movie_info_file.csv"
## youtube動画DL関連
RAW_VIDEOS_DIR = "./data/raw/videos/"
RAW_AUDIO_DIR = "./data/raw/audio/"
## AI生成データ関連
AI_AUDIO_TRANSCRIPTS_TEXT_DIR = "./data/processed/transcripts/"
AI_AUDIO_TRANSCRIPTS_TEXT_FILE = "audio_transcript_output_file.txt"


ARCHIVE_MOVIE_DIR = "./archive/movie/"
ARCHIVE_WAV_DIR = "./archive/wav/"


# ai step 共通
AI_RESPONSE_DIR = "./data/processed/summaries/"
PROMPT_FILE = "prompt.md"

# step 1
STEP1_GEMINI_API_KEY = "AIzaSyClu5hO2LY2qUrNFPHZExSKUj13_R27j5Y"
STEP1_WORK_DIR = "./web_create_step/step1/"
STEP1_AI_RESPONSE_FILE = "step1_ai_response_file.md"

# step 2
STEP2_GEMINI_API_KEY = "AIzaSyAb886Vqo3qVBZ3t3H4-VROWWVkLmGD9-8"
STEP2_WORK_DIR = "./web_create_step/step2/"
STEP2_AI_RESPONSE_FILE = "step2_ai_response_file.json"

# step 3
STEP3_GEMINI_API_KEY = "AIzaSyCdLI3UeQtCa3xNCW6-MwBeNmPUuRp19WU"
STEP3_WORK_DIR = "./web_create_step/step3/"
STEP3_AI_RESPONSE_FILE = "step3_ai_response_file.json"

# step 4
STEP4_GEMINI_API_KEY = "AIzaSyCkzgDe1FVr8zpTk0LUavRu75oApwxfQbY"
STEP4_WORK_DIR = "./web_create_step/step4/"
STEP4_AI_RESPONSE_FILE = "step4_ai_response_file.json"

# step 5
STEP5_GEMINI_API_KEY = "AIzaSyB6sKuhDCIovHSBju352BvtoDjfqUiMDfY"
STEP5_WORK_DIR = "./web_create_step/step5/"
STEP5_AI_RESPONSE_FILE = "step5_ai_response_file.json"

# step 6
STEP6_GEMINI_API_KEY = "AIzaSyAzjzAFykHzurex6Uo1lSCBEhKgQM0xV1s"
STEP6_WORK_DIR = "./web_create_step/step6/"
STEP6_AI_RESPONSE_FILE = "step6_ai_response_file.json"