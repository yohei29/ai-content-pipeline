import time
import random
from src.config import constants
from src.config import settings

class TimeUtils:

  def __init__(self):
    pass

  # ランダムでWaitTimeを施行する
  def wait_randomly(min_sleep=3.0, max_sleep=10.0):
    sleep_time = random.uniform(3.0, 10.0)
    time.sleep(sleep_time)
