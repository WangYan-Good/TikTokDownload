##>> test
##<< test

##<<Base>>
from pathlib import Path

##<<Extension>>
import yaml

##<<Third-part>>

DEFAULT_REFERER = "https://www.douyin.com/"
DEFAULT_USERR_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

class Header():

  ##
  ## Defination and Initialize default
  ##
  referer = str()
  user_agent = str()

  ##
  ## Initialize header and constrcut
  ##
  def __init__(self, header_path:Path = None) -> None:
    if header_path is None:
      print("WARNNING: Invalide input, use default header")
    
    header_dict = dict()
    try:
      ##
      ## Load header configuration
      ##
      if header_path is not None:
        header_dict = self.__parse_header(header_path)
        print("INFO: header initialized succeed!")
      self.referer = header_dict.get("Referer", DEFAULT_REFERER)
      self.user_agent = header_dict.get("User-Agent", DEFAULT_USERR_AGENT)
    except Exception as e:
      print("ERROR: Header init failed: {}".format(e))
      return None
    
  ##
  ## Parse header file
  ##
  def __parse_header(self, header_path:Path = None)->dict:
    if header_path is None:
      return None
    
    try:
      ##
      ## Load header load
      ##
      header_dict = yaml.safe_load(header_path.read_text(encoding="utf-8"))
    except Exception as e:
      print(e)
      return None
    
    return header_dict
  
  ##
  ## Dump header config
  ##
  def dump_header(self):
    print("Header configuration:")
    print("\tReferer: {}".format(self.referer))
    print("\tUser-Agent: {}".format(self.user_agent))

if __name__ == "__main__":
  Header(Path("config/douyin/headers.yml")).dump_header()