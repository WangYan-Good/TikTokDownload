#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import threading
import copy

WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from src.url_list_config import UrlListConfig
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
from requests import request
from requests import exceptions
from random import randint
from time import sleep

import re
from urllib.parse import parse_qs
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse

from src.live_response_dict import Live
import yaml
from src.DataAcquirer import Live as lv
from src.extract import Extractor

from f2.apps.douyin.utils import (
    SecUserIdFetcher,
    AwemeIdFetcher,
    MixIdFetcher,
    WebCastIdFetcher,
    VerifyFpManager,
    create_or_rename_user_folder,
    show_qrcode,
)

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

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml"

#download live command
COMMAND_DOWNLOAD_LIVE = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml -M live"

live_link = re.compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
live_link_self = re.compile(r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?")
live_link_share = re.compile(r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

def post(config:UrlListConfig, section:str):
    print("Download post: start")
    # varify section
    if (config.section.count(section) == 0):
        print ("Have no found the section:{sec}".format(sec=section))
        return

    # download post
    for i in config.getConfigList(section):
        os.system(COMMAND_DOWNLOAD_POST + ' -u ' + i)
    print("Download post: end")

def live(config:UrlListConfig, section:str):
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

def init_f2_config()->dict:
    config = dict()

    # headers
    config.setdefault("headers", dict())

    # proxies
    config.setdefault("proxies", {})

    # msToken
    config.setdefault("msToken", {})

    # ttwid
    config.setdefault("ttwid", {})

async def fetch_user_live_videos(
    kwargs,
    webcast_id: str,
) -> UserLiveFilter:
    """
    用于获取指定用户直播列表。
    (Used to get the list of videos collected by the specified user.)

    Args:
        webcast_id: str: 直播ID (Live ID)

    Return:
        webcast_data: dict: 直播数据字典，包含直播ID、直播标题、直播状态、观看人数、子分区、主播昵称
        (Live data dict, including live ID, live title, live status, number of viewers,
        sub-partition, anchor nickname)
    """

    print(("开始爬取直播: {0} 的数据").format(webcast_id))
    print("===================================")

    async with DouyinCrawler(kwargs) as crawler:
        params = UserLive(web_rid=webcast_id, room_id_str="")
        response = await crawler.fetch_live(params)
        live = UserLiveFilter(response)

    print(
        ("直播ID: {0} 直播标题: {1} 直播状态: {2} 观看人数: {3}").format(
            live.room_id, live.live_title, live.live_status, live.user_count
        )
    )
    print(
        ("子分区: {0} 主播昵称: {1}").format(
            live.sub_partition_title, live.nickname
        )
    )
    print("===================================")
    print(("直播信息爬取结束"))

    return live

# def generate_live_data(data: dict) -> dict:
#     return {
#         "text": "\n".join((f"直播标题: {data["title"]}",
#                             f"主播昵称: {data["nickname"]}",
#                             f"在线观众: {data["user_count_str"]}",
#                             f"观看次数: {data["total_user_str"]}",)),
#         "flv": data["flv_pull_url"],
#         "m3u8": data["hls_pull_url_map"],
#         "best": list(data["flv_pull_url"].values())[0],
#         "preview": data["cover"]}

if __name__ == "__main__":
    live_config = dict()

    # parse config file
    cf = UrlListConfig()
    live_list = cf.getConfigList("live")

    # set f2 config as default
    # config = init_f2_config()
    config = dict()

    # initialize app config
    douyin_conf = ConfigManager(f2.APP_CONFIG_FILE_PATH).get_config("douyin")
    
    # initialize headers
    f2_manager = ConfigManager(f2.F2_CONFIG_FILE_PATH)
    f2_conf = f2_manager.get_config("f2").get("douyin")

    config.setdefault("headers",{})
    config["headers"]["User-Agent"] = f2_conf["headers"].get("User-Agent", "")
    config["headers"]["Referer"] = f2_conf["headers"].get("Referer", "")

    # initialize proxies
    config["proxies"] = f2_conf.get("proxies")

    # download config
    main_manager = ConfigManager(f2.APP_CONFIG_FILE_PATH)
    main_conf_path = get_resource_path(f2.APP_CONFIG_FILE_PATH)
    main_conf = main_manager.get_config("douyin")

    live_list = cf.getConfigList("live")

    for live_share_url in live_list:
        one_url = live_share_url
        try:
            live_config = Live(one_url)

            # make live mode
            if live_config.live_config["live"]["rid"] is True and live_config.live_config["live"]["room_id"] is not None:
                live_data = lv(params=None, room_id=live_config.live_config["live"]["room_id"], sec_user_id=live_config.live_config["live"]["response_url"]["query"]["sec_user_id"], cookie=douyin_conf["cookie"]).run()
                live_data = Extractor().run(live_data, None, "live")[0]
            else:
            # 然后下载直播推流
            # web_id or room_id+sec_user_id
              pass
            # webcast_data = await fetch_user_live_videos(live_config.live_config["web_rid"])
            # receive live data
            if not all(live_data):
                print("have no receive any live data")
                exit(1)
            if live_data["status"] == 4:
                print("received live data status error")
                exit(1)
            # generate_live_data(live_data)
            print(live_data)
            break
        
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.ReadTimeout):
            print("分享链接 {url} 请求数据失败".format(url=one_url))
            continue
        # print("{url} = {reurl}".format(url=one_url, reurl=respone.url))
        # print(params)
    print(live_config.live_config["live"])
    # exit(1)
    print("all download task has been completed")