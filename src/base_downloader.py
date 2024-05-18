##>> test
##<< test

import yaml
from pathlib import Path

HEADERS_CONFIG = "config/headers.yml"

class BaseDownloader():
  
  # headers
  headers = dict()
  headers["Referer"] = None
  headers["User-Agent"] = None

  def __init__(self, headers:dict = None) -> None:
    
    if headers is None:
      self.headers = yaml.safe_load(Path(HEADERS_CONFIG).read_text(encoding="utf-8"))

    print(self.headers)

if __name__ == "__main__":
  BaseDownloader()