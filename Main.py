#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys

WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from src.url_list_config import UrlListConfig

# from src.application.main_web_UI import WebUI

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml -M post"

if __name__ == "__main__":

    # parse config file
    cf = UrlListConfig()

    # download post
    for i in cf.getConfigList("post"):
        try:
            os.system(COMMAND_DOWNLOAD_POST + ' -u ' + i)
            # web_ui = WebUI().deal_live_data(i)
        except Exception as e:
            print("down load live {l} failed: {err}".format(l=i, err=e))
        continue