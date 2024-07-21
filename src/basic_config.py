##>> test
##<< test

##<<Base>>
import os
import sys

##
## Import work space path
##
WORK_SPACE = os.path.dirname(sys.path[0])

import abc
from pathlib import Path

##<<Extension>>
import yaml as yml

##<<Third-part>>
from header import Header

##
## Eefine
##
BASE_CONFIG_PATH = "config/base_config.yml"

##
## Defination sbstract class
##
class BasicConfig(abc.ABC):

  ##
  ## Declare and define default value
  ##
  WORK_SPACE_PATH          = os.getcwd()
  save_path                = "./"
  max_thread               = 0
  folderize                = False
  __base_config_name       = ""
  base_config_path         = ""
  stream_platform          = ""
  login                    = False
  __headers_config_name    = ""
  header_config_path       = ""
  __download_config_name   = ""
  download_config_path     = ""
  platform_config_path     = ""
  __generate_response_path = ""
  save_response            = False
  url_response_path        = ""

  ##
  ## The part of extension
  ##
  header               = Header()

  ##
  ## Initialize basic config
  ##
  def __init__(self, path:Path = BASE_CONFIG_PATH):
    if path is None:
      print("WARNNING: Invalide input, use default basic configuration!")
      path = BASE_CONFIG_PATH

    ##
    ## Initialize basic config
    ##
    try:

      ##
      ## Parse configuration file
      ##
      config           = self.__parse_config(Path(path))
    except Exception as e:
      print("ERROR: Parse basic configuration failed! {}".format(e))
      return None

    try:
      ##
      ## Construct configuration
      ##
      self.save_path                = config.get("save_path", "./")
      self.max_thread               = config.get("max_thread", 0)
      self.folderize                = config.get("folderize", False)
      self.__base_config_name       = config.get("base_config_name", "")
      self.stream_platform          = config.get("stream_platform", "")
      self.login                    = config.get("login", False)
      self.__headers_config_name    = config.get("headers_config_name", "")
      self.__download_config_name   = config.get("download_config_name", "")
      self.__generate_response_path = config.get("generate_response_path", "")
      self.save_response            = config.get("save_response", False)
      
      ##
      ## Construct extension config path
      ##
      self.base_config_path     = self.WORK_SPACE_PATH + "/" + self.__base_config_name
      self.platform_config_path = self.WORK_SPACE_PATH + "/" + self.__base_config_name + "/" + self.stream_platform
      self.header_config_path   = self.platform_config_path + "/" + self.__headers_config_name
      self.download_config_path = self.platform_config_path + "/" + self.__download_config_name
      self.url_response_path    = self.WORK_SPACE_PATH + "/" + self.__base_config_name + "/" + self.__generate_response_path

    except Exception as e:
      print("ERROR: Basic config init failed! {}".format(e))

  ##
  ## parse and genearte download config
  ##
  def __parse_config(self, path:Path = None):
    if path is None:
      print ("ERROR: Invalide configuration path!")
    
    try:
      
      ##
      ## read config file
      ##
      base_config = yml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
      print("ERROR: Parse configuration failed: {}".format(e))
    return base_config
  
  ##
  ## Dump config
  ##
  @abc.abstractmethod
  def dump_config(self, out_putlog_file:Path = False):
    if out_putlog_file is True:
      pass

    print("Basic configuration:")
    print("\tmax thread: {}".format(self.max_thread))
    print("\tfolderize: {}".format(self.folderize))
    print("\tstream platform: {}".format(self.stream_platform))
    print("\tlogin: {}".format(self.login))
    print("\tsave response: {}".format(self.save_response))
    print("\tsave path: {}".format(self.save_path))
    print("\twork space path: {}".format(self.WORK_SPACE_PATH))
    print("\tbase config path: {}".format(self.base_config_path))
    print("\tplatform config path: {}".format(self.platform_config_path))
    print("\turl response path: {}".format(self.url_response_path))