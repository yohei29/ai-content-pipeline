from src.config import constants
from src.config import settings

class WorkPaths:

  def __init__(self):
    pass

  def get_movie_ids_file_path():
    return f"{constants.RAW_METADATA_DIR}{constants.MOVIE_IDS_FILE}"

  def get_movie_data_file_path(youtube_id):
    return f"{constants.RAW_VIDEOS_DIR}{youtube_id}{constants.MP4_EXTENSION}"

  def get_audio_data_file_path(youtube_id):
    return f"{constants.RAW_AUDIO_DIR}{youtube_id}{constants.WAV_EXTENSION}"

  def get_audio_transcripts_text_path(youtube_id):
    return f"{constants.AI_AUDIO_TRANSCRIPTS_TEXT_DIR}{youtube_id}_{constants.AI_AUDIO_TRANSCRIPTS_TEXT_FILE}"

  def put_archive_movie_path(youtube_id):
    return f"{constants.ARCHIVE_MOVIE_DIR}{youtube_id}{constants.MP4_EXTENSION}"

  def put_archive_wav_path(youtube_id):
    return f"{constants.ARCHIVE_WAV_DIR}{youtube_id}{constants.WAV_EXTENSION}"

  def get_prompts_step_prompt_file_path(work_dir):
    return f"{work_dir}{constants.PROMPT_FILE}"

  def get_prompts_step_ai_response_file_path(youtube_id, ai_response_file):
    return f"{constants.AI_RESPONSE_DIR}{youtube_id}_{ai_response_file}"

  def get_movie_score_output_path():
    return f"{constants.MOVIE_SCORE_OUTPUT_DIR}{constants.MOVIE_SCORE_OUTPUT_FILE}"

  def get_movie_score_rejected_output_path():
    return f"{constants.MOVIE_SCORE_OUTPUT_DIR}{constants.MOVIE_SCORE_REJECTED_FILE}"

  def get_movie_score_prompt_file_path():
    return f"{constants.MOVIE_SCORE_WORK_DIR}{constants.PROMPT_FILE}"

  def get_archive_movie_score_path():
    return f"{constants.ARCHIVE_MOVIE_SCORE_DIR}{constants.ARCHIVE_MOVIE_SCORE_FILE}"
