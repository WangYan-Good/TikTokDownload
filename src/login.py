##>> test
##<< test

##<<Base>>
from pathlib import Path

##<<Extension>>
import yaml as yml

##<<Third-part>>
from basic_config import BASE_CONFIG_PATH, BasicConfig


class Login():

  ##
  ## Declare and define default value
  ##
  cookie = ""
  msToken = ""

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
      config = self.__parse_config(Path(path))
      self.cookie = config.get("cookie", "")
      self.msToken = config.get("msToken", "")
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


if __name__ == "__main__":
  login = Login(Path("config/douyin/login.yml")).dump_config()