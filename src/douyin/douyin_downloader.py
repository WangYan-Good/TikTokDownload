# base
from pathlib import Path

# extension

# third part
from basic_config import BASE_CONFIG_PATH
from downloader import Downloader


class DouyinDownloader(Downloader):

  def __init__(self, path: Path = ...) -> None:
    super().__init__(path)

if __name__ == "__main__":
  pass