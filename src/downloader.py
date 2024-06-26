##>> test
##<< test

##<<Base>>
from requests import request, exceptions
from pathlib import Path
from time import sleep
from random import randint
import urllib.request
import re

##<<Extension>>
import yaml as yml

##<<Third-part>>
from basic_config import BasicConfig, BASE_CONFIG_PATH
from header import Header
from url_list_config import UrlListConfig
from login import Login
from live import Live, MAX_TIMEOUT
from verify_fp_manager import VerifyFpManager as VFM

#TODO
import f2
from f2.apps.douyin.utils import TokenManager
from f2.apps.douyin.filter import (
    UserPostFilter,
    UserProfileFilter,
    UserCollectionFilter,
    UserCollectsFilter,
    UserMusicCollectionFilter,
    UserMixFilter,
    PostDetailFilter,
    UserLiveFilter,
    UserLive2Filter,
    GetQrcodeFilter,
    CheckQrcodeFilter,
    UserFollowingFilter,
    UserFollowerFilter,
)

##
## Defination save file name
##
URL_RESPONSE_PATH = ""

##
## Live stream file name
##
LIVE_STREAM_FILE_NAME_RE = r"stream-(\d+)_(\w+)\.(?:flv|m3u8)"

class Downloader(BasicConfig):

  ##
  ## Downloader default configuration
  ##
  type = ""
  __login_config_file_name         = ""
  __download_link_file_name        = ""
  __live_download_config_file_name = ""
  login_config_path                = ""
  download_link_path               = ""
  live_download_config_path        = ""
  flv_clarity                      = 1
  hls_clarity                      = 1

  ##
  ## Login config
  ##
  login_config              = Login()

  ##
  ## Download url list configuration
  ##
  download_url_list         = list()

  ##
  ## share url response
  ##
  share_url_response        = None

  ##
  ## Parameters of request live data
  ##
  live                       = Live()
  parameters_of_request_live = dict()

  ##
  ## Stream url
  ##
  live_stream_url            = ""
  live_stream_name           = ""

  nickname                   = ""

  def __init__(self, path:Path = BASE_CONFIG_PATH) -> None:
    super().__init__(path)
    self.__generate_download_config()

  ##
  ## Generate download config based on base configuration
  ##
  def __generate_download_config(self):

    ##
    ## Initialize downloader header
    ##
    self.header = Header(Path(self.header_config_path))

    ##
    ## Parse download config
    ##
    download_config_dict = self.__parse_config(Path(self.download_config_path))

    ##
    ## Initialize downloader extension
    ##
    self.__login_config_file_name         = download_config_dict.get("login_config_file_name", "")
    self.type                             = download_config_dict.get("type", "")
    self.__live_download_config_file_name = download_config_dict.get("live_download_config_file_name", "")
    self.__download_link_file_name        = download_config_dict.get("download_link_file_name", "")

    ##
    ## Parse login config
    ##
    self.login_config_path = self.platform_config_path + "/" + self.__login_config_file_name
    if self.login is True:
      self.login_config = Login(Path(self.login_config_path))
      

    ##
    ## Parse share link
    ##
    self.download_link_path = self.platform_config_path + "/" +self.__download_link_file_name
    self.download_url_list  = UrlListConfig(self.download_link_path)
    self.download_url_list = self.download_url_list.getConfigList(self.type)

    ##
    ## Construct live download config path
    ##
    self.live_download_config_path = self.platform_config_path + "/" + self.__live_download_config_file_name

  ##
  ## Parse donwload configuration
  ##
  def __parse_config(self, path: Path = None) -> dict:
    config = dict()
    if path is None:
      print ("ERROR: invalide configuration path!")
    
    try:
      ##
      ## read config file
      ##
      config = yml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
      print("parse configuration failed: {}".format(e))
    return config

  ##
  ## Dump downloader configuration
  ##
  def dump_config(self, out_putlog_file: Path = False):
    super().dump_config(out_putlog_file)

    ##
    ## Dump extension configuration
    ##
    self.header.dump_header()
    self.login_config.dump_config()
    print("Downloader configuration:")
    print("\ttype: {}".format(self.type))
    print("\tdownload url: {}".format(self.download_url_list))

  def douyin_downloader(self):
    try:
        # print("\n method:{}\n url:{}\n params:{}\n timeout:{}\n headers:{}\n".format("get", download_params["live_api_share"], live_config.live_config["params"], 10, live_config.live_config["live"]["PC_headers"]))
        response = request(
            method="get",
            url=self.parameters_of_request_live["live_api_share"],
            params=self.parameters_of_request_live,
            timeout=MAX_TIMEOUT,
            headers=self.live.header)
        # 随机延时
        sleep(randint(15, 45) * 0.1)
    except (
            exceptions.ProxyError,
            exceptions.SSLError,
            exceptions.ChunkedEncodingError,
            exceptions.ConnectionError,
    ):
        print("网络异常，请求 {url}?{urlencode(download_params)} 失败")
    except exceptions.ReadTimeout:
        print("网络异常，请求 {url}?{urlencode(download_params)} 超时")
        return None
    return response

  def douyin_live_constructor(self, share_url:str) -> None:
      try:          
          ##
          ## Query response of share url link to server
          ##
          self.share_url_response = self.live.query_share_url(url=share_url, header=self.header)
          self.live.construct_live_data(self.share_url_response)

          ##
          ## Construct paramter to request live data
          ##
          self.parameters_of_request_live["X-Bogus"]        = self.live.x_bogus
          self.parameters_of_request_live["verifyFp"]       = VFM.gen_verify_fp()
          self.parameters_of_request_live["type_id"]        = "0"
          self.parameters_of_request_live["live_id"]        = "1"
          self.parameters_of_request_live["room_id"]        = self.live.room_id
          self.parameters_of_request_live["sec_user_id"]    = self.share_url_response["query"].get("sec_user_id", "")
          self.parameters_of_request_live["version_code"]   = "99.99.99"
          self.parameters_of_request_live["app_id"]         = "1128"
          self.parameters_of_request_live["msToken"]        = TokenManager.gen_real_msToken()
          self.parameters_of_request_live["live_api"]       = "https://live.douyin.com/webcast/room/web/enter/"
          self.parameters_of_request_live["live_api_share"] = "https://webcast.amemv.com/webcast/room/reflow/info/"

          '''
          ##
          ## Save share url response
          ##
          if self.save_response is True:
            URL_RESPONSE_PATH = self.url_response_path + "/" + self.live.room_id[0] + ".yml"
            with open(URL_RESPONSE_PATH, 'w', encoding="utf-8") as f:
               yml.safe_dump(self.parameters_of_request_live, f)
               f.close()
               print("save file {} success!".format(URL_RESPONSE_PATH))
          '''
      except (
              exceptions.ProxyError,
              exceptions.SSLError,
              exceptions.ChunkedEncodingError,
              exceptions.ConnectionError,
              exceptions.ReadTimeout):
          print("分享链接 {url} 请求数据失败".format(url=share_url))
      return None

  ##
  ## Get douyin download live stream
  ##
  def get_douyin_live_download_stream(self, url:str = None)->str:
    if url is None:
      print("Invalide url")
      return None
    
    ##
    ##
    ##
    self.douyin_live_constructor(url)
    
    ##
    ## try receive live stream
    ##
    try:
      ##
      ## request for live stream
      ##
      live_response = request (
          method="get", 
          url=self.parameters_of_request_live["live_api_share"],
          params=self.parameters_of_request_live,
          timeout=self.live.timeout,
          headers=self.live.header)
      # 随机延时
      sleep(randint(15, 45) * 0.1)

      ##
      ## transform response to json format
      ##
      live_response_json = live_response.json()
      live_info = UserLive2Filter(live_response_json)
      if live_info.nickname is not None:
        self.nickname = live_info.nickname
      else:
        self.nickname = "Unknown"
      
      ##
      ## save live information
      ##
      if self.save_response is True:
         LIVE_INFORMATION_PATH = self.url_response_path + "/" + live_info.nickname + ".yml"
        #  print(LIVE_INFORMATION_PATH)
         with open(LIVE_INFORMATION_PATH, 'w') as f:
            yml.safe_dump(live_response_json, f)
            f.close()

      ##
      ## live status
      ##
      if live_info.live_status != 2:
         print("当前 {0} 直播已结束".format(live_info.nickname))
         return None
    except Exception as e:
       print(e)
    
    ##
    ## catch live status success
    ## return live stream
    ##
    try:
      print("当前 {0} 正在直播...".format(live_info.nickname))
      
      ##
      ## FULL_HD1
      ##
      if self.flv_clarity == 1 and live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["FULL_HD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["FULL_HD1"]
      elif self.hls_clarity == 1 and live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["FULL_HD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["FULL_HD1"]
      ##
      ## HD1
      ##
      elif self.flv_clarity == 2 and live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["HD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["HD1"]
      elif self.hls_clarity == 2 and live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["HD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["HD1"]
      ##
      ## SD1
      ##
      elif self.flv_clarity == 3 and live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["SD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["SD1"]
      elif self.hls_clarity == 3 and live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["SD1"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["SD1"]
      ##
      ## SD2
      ##
      elif self.flv_clarity == 4 and live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["SD2"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["flv_pull_url"]["SD2"]
      elif self.hls_clarity == 4 and live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["SD2"] is not None:
        self.live_stream_url = live_response_json["data"]["room"]["stream_url"]["hls_pull_url_map"]["SD2"]

      self.live_stream_name = re.search(LIVE_STREAM_FILE_NAME_RE, self.live_stream_url).group()
    except Exception as e:
       print(e)
       return None
    return self.live_stream_url

  ##
  ## Download post
  ##
  def __download_douyin_post(self):
    pass

  ##
  ## Common download interface
  ##
  def download(self, params:None = ...)->None:
    pass

if __name__ == "__main__":
  downloader = Downloader()
  # downloader.dump_config(False)
  for url in downloader.download_url_list:
    stream_url = downloader.get_douyin_live_download_stream(url)
    if stream_url is None:
      continue
    print(downloader.live_stream_name)

  print("all live download completed!")