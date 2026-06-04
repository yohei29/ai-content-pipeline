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
ARCHIVE_MOVIE_SCORE_DIR = "./archive/movie_score/"
ARCHIVE_MOVIE_SCORE_FILE = "movie_score_archive.csv"

LOGS_DIR = "./logs/"


# ai step 共通
AI_RESPONSE_DIR = "./data/processed/summaries/"
PROMPT_FILE = "prompt.md"

# step 1
STEP1_GEMINI_API_KEY = ""
STEP1_WORK_DIR = "./src/prompts/step1/"
STEP1_AI_RESPONSE_FILE = "step1_ai_response_file.md"

# step 2
STEP2_GEMINI_API_KEY = ""
STEP2_WORK_DIR = "./src/prompts/step2/"
STEP2_AI_RESPONSE_FILE = "step2_ai_response_file.json"

# step 3
STEP3_GEMINI_API_KEY = ""
STEP3_WORK_DIR = "./src/prompts/step3/"
STEP3_AI_RESPONSE_FILE = "step3_ai_response_file.json"

# step 4
STEP4_GEMINI_API_KEY = ""
STEP4_WORK_DIR = "./src/prompts/step4/"
STEP4_AI_RESPONSE_FILE = "step4_ai_response_file.json"

# step 5

STEP5_GEMINI_API_KEY = ""
STEP5_WORK_DIR = "./src/prompts/step5/"
STEP5_AI_RESPONSE_FILE = "step5_ai_response_file.json"

# step 6
STEP6_GEMINI_API_KEY = ""
STEP6_WORK_DIR = "./src/prompts/step6/"
STEP6_AI_RESPONSE_FILE = "step6_ai_response_file.json"

# movie score
MOVIE_SCORE_GEMINI_API_KEY = ""
MOVIE_SCORE_WORK_DIR = "./src/prompts/movie_score/"
MOVIE_SCORE_OUTPUT_DIR = "./data/processed/movie_score/"
MOVIE_SCORE_OUTPUT_FILE = "movie_score.csv"
MOVIE_SCORE_REJECTED_FILE = "movie_score_rejected.csv"