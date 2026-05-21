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
