import asyncio
import io
import os
import re

from nonebot import logger
from pymongo.errors import OperationFailure
from bs4 import BeautifulSoup, Comment
import infinity
import httpx
from infinity.model.chunithm_song import ChuniDifficulty
from infinity import connection

from PIL import Image, ImageDraw


def svdxin_version(version: int) -> str:
    match version:
        case 10000:
            return "01"
        case 10500:
            return "01"
        case 11000:
            return "02"
        case 11500:
            return "02"
        case 12000:
            return "03"
        case 12500:
            return "03"
        case 13000:
            return "04"
        case 13500:
            return "04"
        case 14000:
            return "05"
        case 14500:
            return "05"
        case 15000:
            return "06"
        case 15500:
            return "06"
        case 20000:
            return "07"
        case 20500:
            return "07"
        case 21000:
            return "08"
        case 21500:
            return "08"
        case 22000:
            return "09"
        case 22500:
            return "09"
        case 23000:
            return "10"
        case 23500:
            return "10"


def difficulty_to_short(difficulty: ChuniDifficulty | int) -> str:
    if isinstance(difficulty, ChuniDifficulty):
        difficulty = difficulty.int()
    match difficulty:
        case 0:
            return "bsc"
        case 1:
            return "adv"
        case 2:
            return "exp"
        case 3:
            return "mst"
        case 4:
            return "ult"
        case _:
            return ""

async def sdvxin_automatic_v1():
    # 自动从sdvx.in网站爬取所有曲目的sdvxin_id
    level_names = ["1", "2", "3", "4", "5", "6", "7", "7+", "8", "8+", "9", "9+", "10", "10+", "11", "11+", "12", "12+",
                   "13", "13+", "14", "14+", "15", "15+"]
    # 遍历等级名称
    for level_name in level_names:
        logger.info(f"==={level_name}===")
        # 获取指定等级的页面
        url = f"{infinity.sdvxin_api}chunithm/sort/{level_name}.htm"
        res = httpx.get(url)
        content = res.text
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(content, "html.parser")
        # 查找所有的注释
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        # 遍历所有的注释，输出其歌曲名称（注释内容）和对应的sdvxin_id
        for comment in comments:
            # 找到注释后，获取其前一个<script>标签的src属性值
            script_tag = comment.find_previous_sibling("script")
            # 获取到脚本名，从脚本名中得到歌曲的sdvxin_id
            match = re.search(r'SORT(\d+)\w+\(\);', script_tag.string)
            if match:
                try:
                    sdvxin_id = match.group(1)
                    # 查询数据库中的歌曲数据，如果对应则存入
                    # 通过歌曲名在数据库中查询
                    sd = await connection.query_chunithm_song_by_keyword(comment.string)
                    if sd:
                        # 如果查询到了歌曲，将sdvxin_id存入数据库
                        await connection.chunithm_sdvxin_mapping_collection.insert_one(
                            {
                                "song_id": sd[0].id,
                                "song_name": comment.string,
                                "sdvxin_id": sdvxin_id,
                            },

                        )
                    logger.debug(f"{comment} {sdvxin_id} 存入成功")
                except OperationFailure:
                    logger.warning(f"{comment}存入失败")

async def get_chunithm_preview_v1(mid: int, difficulty: ChuniDifficulty | int = 3):
    # 查找缓存中是否包含该歌曲的图片缓存，如果有则直接返回
    d = difficulty_to_short(difficulty)
    if not os.path.exists(f"./cache"):
        os.mkdir("./cache")
    if os.path.exists(f"./cache/chunithm_chart_preview_{mid}_{d}.png"):
        with open(f"./cache/chunithm_chart_preview_{mid}_{d}.png", "rb") as f:
            return io.BytesIO(f.read())
    # 查询数据库中的歌曲数据
    sd = await connection.query_chunithm_song_by_id(mid)
    if sd:
        # 根据歌曲id查询sdvxin_id
        res = await connection.chunithm_sdvxin_mapping_collection.find_one({"song_id": mid})
        if res:
            # 根据sdvxin_id查询sdvx.in网站的预览图
            url1 = f"{infinity.sdvxin_api}chunithm/{str(svdxin_version(sd.version)) if d != "ult" else "ult"}/bg/{res["sdvxin_id"]}bg.png"
            url2 = f"{infinity.sdvxin_api}chunithm/{str(svdxin_version(sd.version)) if d != "ult" else "ult"}/obj/data{res["sdvxin_id"]}{d}.png"
            # print(url1, url2)
            # 获取两张图片，如果状态为200则返回图片链接
            async with httpx.AsyncClient() as client:
                res1 = await client.get(url1)
                res2 = await client.get(url2)
                print(res1.status_code, res2.status_code)
                if res1.status_code == 200 and res2.status_code == 200:
                    # 使用BytesIO将响应内容转换为文件对象
                    bg_io = io.BytesIO(res1.content)
                    obj_io = io.BytesIO(res2.content)

                    # 将文件对象传递给Pillow
                    bg = Image.open(bg_io)
                    obj = Image.open(obj_io)
                    bg.paste(obj, (0, 0), obj)
                    # 保存图片
                    bg.save(f"./cache/chunithm_chart_preview_{mid}_{d}.png")
                    return bg
    else:
        return None
