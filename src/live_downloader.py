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
    self.__download_config = yaml.safe_load(Path(config).read_text(encoding="utf-8"))
    
    # initialize those member which is null
    self.__download_config["verifyFp"] = VerifyFpManager.gen_verify_fp()
    self.__download_config["msToken"] = TokenManager.gen_real_msToken()
    self.__update_room_id(live.get("room_id", ""))
    self.__update_sec_user_id(live["response_url"]["query"].get("sec_user_id", ""))

    # initialize base downloader
    self.update_headers()

    # initialize member
    self.verifyFp = self.__download_config["verifyFp"]
    self.msToken = self.__download_config["msToken"]
    self.room_id = self.__download_config["room_id"]
    self.sec_user_id = self.__download_config["sec_user_id"]
  
  def __update_room_id (self, room_id):
    self.__download_config["room_id"] = room_id
  
  def __update_sec_user_id (self, sec_user_id):
    self.__download_config["sec_user_id"] = sec_user_id

  def output_all_member(self):
    print("output live downloader:")
    print("headers: {}".format(self.headers))
    print("verifyFp: {}".format(self.verifyFp))
    print("msToken: {}".format(self.msToken))
    print("room_id: {}".format(self.room_id))
    print("sec_user_id: {}".format(self.sec_user_id))

if __name__ == "__main__":
  live = Live("https://v.douyin.com/iFRytwBb/")
  live_downloader = LiveDownloader(live.live_config["live"])
  # print(live_downloader)
  live_downloader.output_all_member()