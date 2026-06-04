from src.config import constants


def merge_ydl_opts(opts: dict | None = None) -> dict:
  """yt-dlp 共通オプション（JS ランタイム等）をマージする。"""
  merged = {
    # deno 未導入環境では node を使う（要 Node 22+、PATH または NODE_PATH）
    "js_runtimes": {"node": {"path": constants.NODE_PATH}},
  }
  if opts:
    merged.update(opts)
  return merged
