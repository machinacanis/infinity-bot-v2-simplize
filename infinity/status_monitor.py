import asyncio
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Any

import httpx
import nonebot
import psutil
from nonebot.adapters.onebot.v11 import Bot as OnebotV11Bot

import infinity

start_timestamp = datetime.fromtimestamp(0)
message_timestamps = []
hourly_message_processed = []


def message_occurred():
    message_timestamps.append(datetime.now())


def get_message_count_last_hour():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    # 处理掉一个小时前的消息时间戳防止内存泄漏
    global message_timestamps
    message_timestamps = [timestamp for timestamp in message_timestamps if timestamp > one_hour_ago]
    # 返回一个小时内的消息数量
    return len(message_timestamps)

def init_hourly_message_processed():
    # 这个函数需要在机器人启动时初始化！！！
    # 建立一个线程，每个小时运行一次get_message_count_last_hour()，并将返回值存入hourly_message_processed
    def run():
        while True:
            count = get_message_count_last_hour()
            if count != 0:
                hourly_message_processed.append(count)
            time.sleep(3600)  # Sleep for one hour

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()

def get_hourly_message_processed():
    # 计算每小时平均处理消息数
    if len(hourly_message_processed) == 0:
        return get_message_count_last_hour()
    return sum(hourly_message_processed) / len(hourly_message_processed)


async def get_qq_groups_joined_count(bot: OnebotV11Bot) -> int:
    """
    获取机器人加入的QQ群数量
    """
    try:
        group_list = await bot.get_group_list()
    except nonebot.adapters.onebot.v11.exception.ActionFailed as e:
        return 0
    return len(group_list)


def get_memory_usage() -> tuple[Any, Any, Any, Any, Any]:
    """
    获取机器人当前占用的内存大小和总内存占用以及总内存大小，以及对应的两个数值的内存使用率，返回5个数值构成的元组，单位为MB
    """
    pid = os.getpid()
    p = psutil.Process(pid)

    memory_used_by_bot = round(p.memory_info().rss / 1024 / 1024, 1)
    memory_used_all = round(psutil.virtual_memory().used / 1024 / 1024, 1)
    memory_total = round(psutil.virtual_memory().total / 1024 / 1024, 1)
    memory_used_by_bot_precent = round(memory_used_by_bot / memory_total * 100, 1)
    memory_used_all_precent = round(memory_used_all / memory_total * 100, 1)
    return memory_used_by_bot, memory_used_all, memory_total, memory_used_by_bot_precent, memory_used_all_precent


def set_start_time():
    global start_timestamp
    start_timestamp = datetime.now()


def get_running_time() -> timedelta:
    """
    获取机器人运行时间
    """
    return datetime.now() - start_timestamp

async def check_diving_fish() -> bool:
    resp = httpx.get(infinity.df_api + "maimaidxprober/alive_check")
    if resp.status_code != 200:
        return False
    if resp.json()["message"] != "ok":
        return False
    return True

async def check_lxns() -> bool:
    resp = httpx.get(infinity.lx_api + "maimai/song/list")
    if resp.status_code != 200:
        return False
    return True

async def check_fanyu() -> bool:
    resp = httpx.get(infinity.fanyu_api + "maimai/alias.json")
    if resp.status_code != 200:
        return False
    return True

async def check_wahlap() -> bool:
    resp = httpx.get(infinity.wahlap_arcade_api + "maidx/rest/location")
    if resp.status_code != 200:
        return False
    return True