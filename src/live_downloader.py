##>> test
##<< test
import os
import sys
# WORK_SPACE = os.path.dirname(sys.path[0])
# sys.path.append(os.path.join(WORK_SPACE))
import yaml
from pathlib import Path
import threading
import urllib.request
from urllib.error import ContentTooShortError 

# third part
from downloader import Downloader, BASE_CONFIG_PATH
from live_response_dict import Live

# LIVE_DOWNLOAD_CONFIG = "config/live_download_config.yml"

max_count = 0
live_list                = list()
download_threading_count = int()
active_download_status = list()
active_download_list = list()

# extension from Downloader
class LiveDownloader(Downloader):
  ##
  ## LiveDownloader default configuration
  ## TODO
  ##
  # max_download_number    = 0
  # current_download_count = 0
  # active_download_task   = list()

  def __init__(self, path:Path = BASE_CONFIG_PATH) -> None:
    super().__init__(path)

  def create_download_task(self, url):
    global download_threading_count
    task = ("get", self.live_stream_url, self.save_path, self.live_stream_name, True, self.login_config.proxies.get_proxies(), self.live.header, self.live.timeout)

    ##
    ## chache threading & status
    ##
    active_download_list[self.download_url_list.index(url)] = threading.Thread(target=__request_file__, args=task)
    active_download_status[self.download_url_list.index(url)] = True
    
    ##
    ## start threading
    ##
    download_task = active_download_list[self.download_url_list.index(url)]
    download_threading_count += 1
    download_task.start()

  def download_live_stream(self, url):

    ##
    ## Detect actived url
    ##
    try:
      self.active_download_task.index(url)
      print("{} has been created, skip...")
      return None
    except ValueError as ve:
      self.active_download_task.append(url)
    
    ##
    ## Check max task number
    ##
    if self.max_download_number == 0 or self.max_download_number > self.current_download_count:
      ##
      ## Create download live stream threading
      ##
      task_args = (self, "get", url, )
      download_task = threading.Thread(target=__request_file__, args=task_args)
      
      ##
      ## current download task + 1
      ##
      self.current_download_count += 1
      download_task.start()

def __request_file__(
  method: str,
  url: str,
  save_path: str,
  file_name: str,
  # nickname: str,
  # params,
  stream: bool,
  proxies,
  headers: dict = None,
  timeout = 10,
  ):
  try:
    global download_threading_count
    global active_download_status
    print("\n path:{}\n method:{}\n url:{}\n stram:{}\n proxies:{}\n headers:{}\n timeout:{}\n start download:".format(save_path + "/" + file_name, method, url, stream, proxies, headers, timeout))
    print("当前总下载数：{}".format(download_threading_count))
    auto_down (url, save_path, file_name, 0)
    
    # reset threading status
    download_threading_count -= 1
    active_download_status[list(live_list).index(url)] = False
    # print("\n name:{}\n url:{}\n download complete!\n".format(nickname, url))    
    print("当前总下载数：{}".format(download_threading_count))
  except Exception as e:
      print("request error: {err}".format(err=e))
      return None

def auto_down (url: str, fp: str, fn: str, retry_times: int):
  try:
      if retry_times == 0:
          file_name = fp + "/" + fn
      else:
          file_name = fp + "/" + "re_" + retry_times + "_" + fn
      urllib.request.urlretrieve (url, file_name)
  except ContentTooShortError:
      retry_times += 1
      auto_down (url, fp, fn, retry_times)

  ##
  ## Get attribute value
  ## example: "$.data.room.owner.nickname"
  ##
  def _get_attr_value(self, jsonpath_expr):
      expr = parse(jsonpath_expr)
      # expr = parser.parse(jsonpath_expr)
      result = expr.find(self._data)
      if result:
          return (
              [match.value for match in result]
              if len(result) > 1
              else result[0].value
          )
      return None

if __name__ == "__main__":
  live = LiveDownloader()
  # live.dump_config()

  live_list = live.download_url_list.copy()
  active_download_status = [False] * len(live.download_url_list)
  active_download_list = [None] * len(live.download_url_list)
  download_threading_count = 0

  for live_url in live.download_url_list:
    stream_url = live.get_douyin_live_download_stream(live_url)
    if stream_url is None:
      continue
    # print(live.live_stream_name)
    live.create_download_task(live_url)
    print(stream_url)