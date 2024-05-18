#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import threading
# import ThreadPoolExecutor
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

from f2.apps.douyin.dl import DouyinDownloader
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
import urllib.request
from urllib.error import ContentTooShortError 
from random import randint
from time import sleep

import re
from urllib.parse import parse_qs
# from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse

import yaml
import json

#download post command
COMMAND_DOWNLOAD_POST = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml"

#download live command
COMMAND_DOWNLOAD_LIVE = "python3 DouYinTool.py -c ./f2/f2/conf/app.yaml -M live"

live_link = re.compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
live_link_self = re.compile(r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?")
live_link_share = re.compile(r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

# http://pull-flv-f26.douyincdn.com/stagereplay/stream-114726907443675823_or4.flv
download_file_name = r"stream-(\d+)_(\w+)\.(?:flv|m3u8)"
# re.compile(r"\S*?http://pull-flv\S+\.douyincdn\.com/\S+(stream-[0-9]+_[a-z]+[0-9]*\.[a-z|0-9]+).*")

def auto_down (url: str, fp: str, retry_times: int):
    try:
        if retry_times != 0:
            file_name = fp + "_" + retry_times + ".flv"
        else:
            file_name = fp + re.search(download_file_name, url).group()
        urllib.request.urlretrieve (url, file_name)
    except ContentTooShortError:
        retry_times += 1
        auto_down (url, fp, retry_times)

def request_file (
    method: str,
    url: str,
    nickname: str,
    # params,
    stream: bool,
    proxies,
    headers: dict = None,
    timeout = 10,
    ):
    try:
        print("\n name:{}\n method:{}\n url:{}\n stram:{}\n proxies:{}\n headers:{}\n timeout:{}\n start download:".format(nickname, method, url, stream, proxies, headers, timeout))
        # urllib.request.urlretrieve(url, "/home/userid/Videos/" + nickname +".flv")
        auto_down (url, "/mnt/share/md/md10/Vedio/douyin/live/", 0)
        print("\n name:{}\n url:{}\n download complete!\n".format(nickname, url))
        '''
        with request(method=method, url=url, stream=stream, proxies=proxies, headers=headers, timeout=timeout) as response:
            # print(response)
            if not (content := int(response.headers.get('content-length',  0))) and not False:
                print("{u} 响应内容为空".format(u=url))
                exit(1)
            if response.status_code != 200:
                print("{u} 响应码异常: {status_code}".format(url, response.status_code))
                exit(1)
            elif all((104857600, content, content > 104857600)):
                print("文件大小超出限制，跳过下载")
                exit(1)
            print(response)
            exit(1)
        download()
                    # download_file
                        # temp,
                        # actual,
                        # show,
                        # id_,
                        # response,
                        # content,
                        # count,
                        # progress
        '''
    
    except Exception as e:
        print("request error: {err}".format(err=e))
        exit(1)

def download():
    pass
'''
def download_file(
        self,
        temp: str,   # temp path
        actual: str, # actual path
        show: str,
        id_: str,     # id
        response,
        content: int,
        count: SimpleNamespace,
        progress: Progress) -> bool:
    task_id = progress.add_task(
        show, total=content or None)
    try:
        with temp.open("wb") as f:
            for chunk in response.iter_content(chunk_size=self.chunk):
                f.write(chunk)
                progress.update(task_id, advance=len(chunk))
            progress.remove_task(task_id) 
    except exceptions.ChunkedEncodingError:
        progress.remove_task(task_id)
        self.log.warning(f"{show} 由于网络异常下载中断")
        self.delete_file(temp)
        return False
    self.save_file(temp, actual)
    self.log.info(f"{show} 文件下载成功")
    self.log.info(f"文件路径 {actual.resolve()}", False)
    self.blacklist.update_id(id_)
    self.add_count(show, id_, count)
    return True
'''

if __name__ == "__main__":
    kwargs = dict()
    download_params = dict()

    # parse config file
    cf = UrlListConfig()
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
    print("live count:{}\n list: {}".format(len(live_list), live_list))

    for live_share_url in live_list:
        one_url = live_share_url # "https://v.douyin.com/iF32SFoa/" # live_share_url
        # one_url = "https://v.douyin.com/i2mmYRQp/"
        try:            
            live_config = Live(one_url)
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
        # live_config.update_config()

        try:
            # print("\n method:{}\n url:{}\n params:{}\n timeout:{}\n headers:{}\n".format("get", download_params["live_api_share"], live_config.live_config["params"], 10, live_config.live_config["live"]["PC_headers"]))
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
        # print(response)
        try:
            # 获取直播推流
            res_js = response.json()
            # print(type(res_js))
            print("\n")
            live = UserLive2Filter(res_js)
            print("主播昵称: {0} 开播时间: {1} 直播流清晰度: {2}".format(live.nickname, live.create_time, "、".join([f"{key}: {value}" for key, value in live.resolution_name.items()]),))
            print("直播ID: {0} 直播标题: {1} 直播状态: {2} 观看人数: {3}".format(live.web_rid, live.live_title, live.live_status, live.user_count))
            # with open("config/"+live.nickname+".yml", 'w') as f:
            #     yaml.safe_dump(res_js, f)
            # anchor = yaml.safe_load(response)
            # print(res_js)

            if live.live_status != 2:
                print("当前 {0} 直播已结束".format(live.nickname))
                continue
                
            # 加入 user db

            # 创建下载任务
            task = ("get", res_js["data"]["room"]["stream_url"]["flv_pull_url"]["FULL_HD1"], live.nickname, True, f2_proxies, live_config.live_config["live"]["PC_headers"], 0)
            download_task = threading.Thread(target=request_file, args=task)
            download_task.start()

        except exceptions.JSONDecodeError:
            if response.text:
                print("响应内容不是有效的 JSON 格式：{response.text}")
            else:
                print("响应内容为空，可能是接口失效或者 Cookie 失效，请尝试更新 Cookie")

    print("all download task has been completed")