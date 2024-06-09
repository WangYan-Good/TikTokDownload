##>> test
##<< test

##<<Base>>
from pathlib import Path

##<<Extension>>
import yaml as yml

##<<Third-part>>
from basic_config import BasicConfig, BASE_CONFIG_PATH
from header import Header
from url_list_config import UrlListConfig
from login import Login

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

  ##
  ## Login config
  ##
  login_config              = Login()

  ##
  ## Download url list configuration
  ##
  download_url_list         = list()

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

if __name__ == "__main__":
  Downloader().dump_config(False)