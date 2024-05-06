#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import threading
import copy

WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from src.url_list_config import UrlListConfig
from src.live_response_dict import Live
import string

import f2
from f2.utils.conf_manager import ConfigManager
from f2.utils.utils import (
    split_dict_cookie,
    get_resource_path,
    get_cookie_from_browser,
    check_invalid_naming,
    merge_config,
)
from f2.utils.xbogus import XBogus as XB

from f2.apps.douyin.utils import TokenManager, VerifyFpManager
from f2.apps.douyin.crawler import DouyinCrawler
from f2.apps.douyin.filter import (
    UserPostFilter,
    UserProfileFilter,
    UserCollectionFilter,
    UserCollectsFilter,
    UserMusicCollectionFilter,
    UserMixFilter,
    PostDetailFilter,
    UserLiveFilter,
    UserLive2Filter,
    GetQrcodeFilter,
    CheckQrcodeFilter,
    UserFollowingFilter,
    UserFollowerFilter,
)
from f2.apps.douyin.model import (
    UserPost,
    UserProfile,
    UserLike,
    UserCollection,
    UserCollects,
    UserCollectsVideo,
    UserMusicCollection,
    UserMix,
    PostDetail,
    UserLive,
    UserLive2,
    LoginGetQr,
    LoginCheckQr,
    UserFollowing,
    UserFollower,
)

from requests import request
from requests import exceptions
from random import randint
from time import sleep

import re
from urllib.parse import parse_qs
# from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse

import yaml

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml"

#download live command
COMMAND_DOWNLOAD_LIVE = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml -M live"

live_link = re.compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
live_link_self = re.compile(r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?")
live_link_share = re.compile(r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

if __name__ == "__main__":
    kwargs = dict()
    download_params = dict()

    # parse config file
    cf = UrlListConfig()
    # live_list = cf.getConfigList("live")
    # for url in live_list:
    #     os.system(COMMAND_DOWNLOAD_LIVE + " -u " + url)
    # print("all download task has been completed")

    # post_thread = threading.Thread(target=post, args=(cf, "post"))
    # live_thread = threading.Thread(target=live, args=(cf, "live"))

    # start thread
    # post_thread.start()
    # live_thread.start()

    # wait for thread end
    # post_thread.join()
    # live_thread.join()

    main_manager = ConfigManager(f2.APP_CONFIG_FILE_PATH)
    main_conf_path = get_resource_path(f2.APP_CONFIG_FILE_PATH)
    main_conf = main_manager.get_config("douyin")
    # print(yaml.safe_load(main_conf["cookie"]).get("msToken"))

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
        pass

    one_url = "https://v.douyin.com/iFemNNTW/" # live_share_url
    try:
        # # one_url_response = Live(one_url)
        # # print(one_url_response.live_config)
        # respone = request ("get", one_url, timeout=10, headers=kwargs["headers"])
        # url = urlparse(respone.url)
        # print(respone.url)
        # # print(XB(user_agent=ua).getXBogus(respone.url)[1])
        # # 随机延时
        # sleep(randint(15, 45) * 0.1)

        # # 解析直播链接
        # if u := live_link.findall(respone.url):
        #     params = generate_live_params(True, u)
        # elif u := live_link_self.findall(respone.url):
        #     params = generate_live_params(True, u)
        # elif u := live_link_share.findall(respone.url):
        #     params = generate_live_params(False, extract_sec_user_id(u))
        
        live_config = Live(one_url)
        # print(live_config.live_config["live"])

    except (
            exceptions.ProxyError,
            exceptions.SSLError,
            exceptions.ChunkedEncodingError,
            exceptions.ConnectionError,
            exceptions.ReadTimeout):
        print("分享链接 {url} 请求数据失败".format(url=one_url))
        # continue
    # print("{url} = {reurl}".format(url=one_url, reurl=respone.url))
    download_params["verifyFp"] = VerifyFpManager.gen_verify_fp()
    download_params["type_id"] = "0"
    download_params["live_id"] = "1"
    download_params["room_id"] = live_config.live_config["live"].get("room_id", "")
    download_params["sec_user_id"] = live_config.live_config["live"]["response_url"]["query"].get("sec_user_id", "")
    download_params["version_code"] = "99.99.99"
    download_params["app_id"] = "1128"
    download_params["msToken"] = TokenManager.gen_real_msToken()

    respone = request ("get", one_url, timeout=10, headers=live_config.live_config["live"]["headers"])
    download_params["X-Bogus"] = XB(user_agent=live_config.live_config["live"]["headers"].get("User-Agent", "")).getXBogus(respone.url)
    download_params["live_api"] = "https://live.douyin.com/webcast/room/web/enter/"
    download_params["live_api_share"] = "https://webcast.amemv.com/webcast/room/reflow/info/"

    live_config.live_config["params"] = download_params
    live_config.update_config()
    # DouyinCrawler:
    # headers["User-Agent"]
    # cookie
    # proxies

    try:
        response = request(
            method="get",
            url=download_params["live_api_share"],
            params=live_config.live_config["params"],
            timeout=10,
            headers=live_config.live_config["live"]["PC_headers"])
        # 随机延时
        sleep(randint(15, 45) * 0.1)
    except (
            exceptions.ProxyError,
            exceptions.SSLError,
            exceptions.ChunkedEncodingError,
            exceptions.ConnectionError,
    ):
        print("网络异常，请求 {url}?{urlencode(download_params)} 失败")
    except exceptions.ReadTimeout:
        print("网络异常，请求 {url}?{urlencode(download_params)} 超时")
        exit(1)
    print(response)
    try:
        res_js = response.json()
        print(res_js)
    except exceptions.JSONDecodeError:
        if response.text:
            print("响应内容不是有效的 JSON 格式：{response.text}")
        else:
            print("响应内容为空，可能是接口失效或者 Cookie 失效，请尝试更新 Cookie")

    print("all download task has been completed")