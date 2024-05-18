##>> test
##<< test
import os
import sys
import yaml
from pathlib import Path

# F2
from f2.apps.douyin.utils import TokenManager, VerifyFpManager

# third part
WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from src.base_downloader import BaseDownloader
from src.live_response_dict import Live

LIVE_DOWNLOAD_CONFIG = "config/live_download_config.yml"

# extension from BaseDownloader
class LiveDownloader(BaseDownloader):
  
  def __init__(self, live:dict, config:str = LIVE_DOWNLOAD_CONFIG) -> None:
    self.download_config = yaml.safe_load(Path(config).read_text(encoding="utf-8"))
    
    # initialize those member which is null
    self.download_config["verifyFp"] = VerifyFpManager.gen_verify_fp()
    self.download_config["msToken"] = TokenManager.gen_real_msToken()
    self.__update_room_id(live.get("room_id", ""))
    self.__update_sec_user_id(live["response_url"]["query"].get("sec_user_id", ""))
  
  def __update_room_id (self, room_id):
    self.download_config["room_id"] = room_id
  
  def __update_sec_user_id (self, sec_user_id):
    self.download_config["sec_user_id"] = sec_user_id

if __name__ == "__main__":
  live = Live("https://v.douyin.com/iFRytwBb/")
  live_downloader = LiveDownloader(live.live_config["live"])
  print(live_downloader.download_config)