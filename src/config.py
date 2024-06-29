##>> test
##<< test

##<<Base>>
import abc
from pathlib import Path

##<<Extension>>
import yaml as yml

##<<Third-part>>
from basic_config import BasicConfig

##
## Eefine
##
BASE_CONFIG_PATH = "config/base_config.yml"

class Config(BasicConfig):

  ##
  ## Initialize class and generate configuration
  ##
  def __init__(self, path:Path = BASE_CONFIG_PATH):
    if path is None:
      print("invalide configuration!")
    
    ##
    ## Initialize super class
    ##
    super().__init__(path)

  ##
  ## Dump configuration
  ##
  def dump_config(self):
    super().dump_config()

if __name__ == "__main__":
  config = Config()
  config.dump_config()
  # bc = BasicConfig(config.base_config)