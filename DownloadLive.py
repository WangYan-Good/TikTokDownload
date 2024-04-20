#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import threading
import copy

WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from Config import Config
import string

import f2
# from f2.utils.conf_manager import ConfigManager
# from f2.utils.utils import (
#     split_dict_cookie,
#     get_resource_path,
#     get_cookie_from_browser,
#     check_invalid_naming,
#     merge_config,
# )
# from requests import request
# from requests import exceptions
# from random import randint
# from time import sleep

import re
# from urllib.parse import parse_qs
# from urllib.parse import quote
# from urllib.parse import urlencode
# from urllib.parse import urlparse

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml"

#download live command
COMMAND_DOWNLOAD_LIVE = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml -M live"

live_link = re.compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
live_link_self = re.compile(r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?")
live_link_share = re.compile(r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

def post(config:Config, section:str):
    print("Download post: start")
    # varify section
    if (config.section.count(section) == 0):
        print ("Have no found the section:{sec}".format(sec=section))
        return

    # download post
    for i in config.getConfigList(section):
        os.system(COMMAND_DOWNLOAD_POST + ' -u ' + i)
    print("Download post: end")

def live(config:Config, section:str):
    live_thread_list = list()
    print("Download live: start")
    # varify section
    if (config.section.count(section) == 0):
        print ("Have no found the section:{sec}".format(sec=section))
        return

    # download post
    for i in config.getConfigList(section):
        live_thread_list.append(threading.Thread(target=os.system, args=(COMMAND_DOWNLOAD_LIVE + ' -u ' + i)))
        live_thread_list[-1].start()
    
    # wait for all thread complete
    for lt in live_thread_list:
        lt.join()
    print("Download live: end")

def extract_sec_user_id(urls: list[str]) -> list[list]:
    data = []
    for url in urls:
        url = urlparse(url)
        query_params = parse_qs(url.query)
        data.append([url.path.split("/")[-1],
                        query_params.get("sec_user_id", [""])[0]])
    return data

def generate_live_params(rid: bool, ids: list[list]) -> list[dict]:
    if not ids:
        print("提取 web_rid 或者 room_id 失败！")
        return []
    if rid:
        return [{"web_rid": id_} for id_ in ids]
    else:
        return [{"room_id": id_[0], "sec_user_id": id_[1]} for id_ in ids]

if __name__ == "__main__":
    kwargs = dict()

    # parse config file
    cf = Config()
    live_list = cf.getConfigList("live")
    for url in live_list:
        os.system(COMMAND_DOWNLOAD_LIVE + " -u " + url)
    print("all download task has been completed")

    # post_thread = threading.Thread(target=post, args=(cf, "post"))
    # live_thread = threading.Thread(target=live, args=(cf, "live"))

    # start thread
    # post_thread.start()
    # live_thread.start()

    # wait for thread end
    # post_thread.join()
    # live_thread.join()
'''
    main_manager = ConfigManager(f2.APP_CONFIG_FILE_PATH)
    main_conf_path = get_resource_path(f2.APP_CONFIG_FILE_PATH)
    main_conf = main_manager.get_config("douyin")

    # 读取f2低频配置文件
    f2_manager = ConfigManager(f2.F2_CONFIG_FILE_PATH)

    f2_conf = f2_manager.get_config("f2").get("douyin")
    f2_proxies = f2_conf.get("proxies")

    # 更新主配置文件中的headers参数
    kwargs.setdefault("headers", {})
    kwargs["headers"]["User-Agent"] = f2_conf["headers"].get("User-Agent", "")
    kwargs["headers"]["Referer"] = f2_conf["headers"].get("Referer", "")

    # print(kwargs)

    live_list = cf.getConfigList("live")

    for live_share_url in live_list:
        one_url = live_share_url
        try:
            respone = request ("get", one_url, timeout=10, headers=kwargs["headers"])
            # 随机延时
            sleep(randint(15, 45) * 0.1)

            # 解析直播链接
            if u := live_link.findall(respone.url):
                params = generate_live_params(True, u)
            elif u := live_link_self.findall(respone.url):
                params = generate_live_params(True, u)
            elif u := live_link_share.findall(respone.url):
                params = generate_live_params(False, extract_sec_user_id(u))

        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.ReadTimeout):
            print("分享链接 {url} 请求数据失败".format(url=one_url))
            continue
        # print("{url} = {reurl}".format(url=one_url, reurl=respone.url))
        print(params)

    print("all download task has been completed")
'''