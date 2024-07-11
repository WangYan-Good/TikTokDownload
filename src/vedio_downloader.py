# base
from pathlib import Path

# extension

# third part
from downloader import Downloader, BASE_CONFIG_PATH

class VedioDownloader(Downloader):
  ##
  ## parameter
  ##

  ##
  ## initialize
  ##
  def __init__(self, path:Path = BASE_CONFIG_PATH) -> None:
    pass
