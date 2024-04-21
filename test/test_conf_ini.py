#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))

from src.url_list_config import UrlListConfig

DEFAULT_CONF_PATH = "config/conf.ini"

if __name__ == "__main__":
  url_list_config = UrlListConfig(DEFAULT_CONF_PATH)
  post_list = url_list_config.getConfigList("live")
  print(post_list)