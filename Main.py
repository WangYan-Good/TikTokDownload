#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys

WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from Config import Config

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml"

if __name__ == "__main__":

    # parse config file
    cf = Config()

    # download post
    for i in cf.getConfigList("post"):
        os.system(COMMAND_DOWNLOAD_POST + ' -u ' + i)