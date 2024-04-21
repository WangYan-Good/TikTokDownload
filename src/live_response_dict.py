##>> test
import os
import sys
WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
##<< test
import f2
from f2.utils.conf_manager import ConfigManager

from pathlib import Path
import yaml

from requests import request
from time import sleep
from random import randint

from urllib.parse import urlparse
from urllib.parse import parse_qs
import yaml

LIVE_CONFIG_PATH = "config/live.yml"
MAX_TIMEOUT = 10

class Live():
  
  def __init__(self, url:str) -> None:
    # check url
    if url is None:
      print("Have no detect live url")

    # load default config formal
    self.live_config = yaml.safe_load(Path(LIVE_CONFIG_PATH).read_text(encoding="utf-8"))
    
    # initialize live link share
    self.live_config["live"]["live_link_share"] = url
    
    # request response url
    self.live_config["live"]["response_url"] = self.get_response_url(url)
  
  def get_response_url(self, share_url:str) -> dict:
    response_url = dict()
    # request url
    response = request("get", share_url, timeout=MAX_TIMEOUT, headers=self.live_config["live"]["headers"])
    
    # random delay
    sleep(randint(15, 45) * 0.1)

    # response url
    url = urlparse(response.url)
    response_url["scheme"] = url.scheme
    response_url["netloc"] = url.netloc
    response_url["path"] = url.path
    response_url["params"] = url.params

    # url query
    url_query = str(parse_qs(url.query)).replace("\\", "")
    response_url["query"] = yaml.safe_load(url_query)
    return response_url

  def __init_live_header__(self, headers:dict):
    # ['User-Agent', 'Referer']
    pass

  def __init_live_proxies__(self):
    # ['http', 'https']
    pass

  def __init_live_msToken__(self):
    # ['url', 'magic', 'version', 'dataType', 'strData', 'User-Agent']
    pass

  def __init_live_ttwid__(self):
    # ['url', 'data']
    pass

if __name__ == "__main__":
  live_config = Live("https://v.douyin.com/iF32SFoa/")
  print(live_config.live_config)
