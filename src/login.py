##>> test
##<< test

##<<Base>>
from pathlib import Path

##<<Extension>>
import yaml as yml

##<<Third-part>>
from basic_config import BASE_CONFIG_PATH, BasicConfig

class Proxies():
  ##
  ## Declare and define default value
  ##
  http    = None
  https   = None

  def get_proxies(self)->dict:
    px          = dict()
    px["http"]  = self.http
    px["https"] = self.https

    return px

  ##
  ## Dump configuration
  ##
  def dump_config(self):
    print("Proxies configuration:")
    print("\thttp: {}".format(self.http))
    print("\thttps: {}".format(self.https))

class Login():

  ##
  ## Declare and define default value
  ##
  cookie  = ""
  msToken = ""
  proxies = Proxies()

  ##
  ## Initialize and construc class
  ##
  def __init__(self, path: Path = None):
    if path is None:
      return None
    
    ##
    ## Parse configuration file
    ##
    try:
      config             = self.__parse_config(Path(path))
      self.cookie        = config.get("cookie", "")
      self.msToken       = config.get("msToken", "")
      self.proxies.http  = dict(config.get("proxies", "")).get("http", None)
      self.proxies.https = dict(config.get("proxies", "")).get("https", None)
    except Exception as e:
      print(e)
  ##
  ## parse and genearte download config
  ##
  def __parse_config(self, path:Path = None)->dict:
    if path is None:
      print ("ERROR: invalide configuration path!")
    
    try:
      
      ##
      ## read config file
      ##
      base_config = yml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
      print("parse configuration failed: {}".format(e))
    return base_config

  ##
  ## Dump configuration
  ##
  def dump_config(self):
    print("Login configuration:")
    print("\tcookie: {}".format(self.cookie))
    print("\tmsToken: {}".format(self.msToken))
    self.proxies.dump_config()


if __name__ == "__main__":
  login = Login(Path("config/douyin/login.yml")).dump_config()