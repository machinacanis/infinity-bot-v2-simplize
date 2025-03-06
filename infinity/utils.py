import re
from datetime import timedelta

from nonebot import Bot

from infinity import global_cache


def is_dx(mid: int):
    if 10000 <= mid < 100000:
        return True
    return False


def mai_get_b40_coeff(percentage: float) -> float:
    """根据达成率获取b40系数"""
    match percentage:
        case p if p >= 100.5:
            return 14
        case p if p >= 100.4999:
            return 13.9
        case p if p >= 100:
            return 13.5
        case p if p >= 99.9999:
            return 13.4
        case p if p >= 99.5:
            return 13.2
        case p if p >= 99:
            return 13
        case p if p >= 98.9999:
            return 12.9
        case p if p >= 98:
            return 12.7
        case p if p >= 97:
            return 12.5
        case p if p >= 96.9999:
            return 11
        case p if p >= 94:
            return 10.5
        case p if p >= 90:
            return 9.5
        case p if p >= 80:
            return 8.5
        case p if p >= 79.9999:
            return 8
        case p if p >= 75:
            return 7.5
        case p if p >= 70:
            return 7
        case p if p >= 60:
            return 6
        case p if p >= 50:
            return 5
        case p if p >= 40:
            return 4
        case p if p >= 30:
            return 3
        case p if p >= 20:
            return 2
        case p if p >= 10:
            return 1
        case _:
            return 0


def mai_get_b50_coeff(percentage: float) -> float:
    """根据达成率获取b50系数"""
    match percentage:
        case p if p >= 100.5:
            return 22.4
        case p if p >= 100.4999:
            return 22.2
        case p if p >= 100:
            return 21.6
        case p if p >= 99.9999:
            return 21.4
        case p if p >= 99.5:
            return 21.1
        case p if p >= 99:
            return 20.8
        case p if p >= 98.9999:
            return 20.6
        case p if p >= 98:
            return 20.3
        case p if p >= 97:
            return 20
        case p if p >= 96.9999:
            return 17.6
        case p if p >= 94:
            return 16.8
        case p if p >= 90:
            return 15.2
        case p if p >= 80:
            return 13.6
        case p if p >= 79.9999:
            return 12.8
        case p if p >= 75:
            return 12
        case p if p >= 70:
            return 11.2
        case p if p >= 60:
            return 9.6
        case p if p >= 50:
            return 8
        case p if p >= 40:
            return 6.4
        case p if p >= 30:
            return 4.8
        case p if p >= 20:
            return 3.2
        case p if p >= 10:
            return 1.6
        case _:
            return 0


def maimai_ra_calculate(decimal: float, acc: float):
    """计算舞萌游戏中指定定数谱面对应成绩的Rating结果，传入的定数格式类似15.0，传入的成绩（达成率）格式类似101.0，返回的结果是一个元组，第一个元素是b40系数计算的Rating，第二个元素是b50系数计算的Rating"""
    # 获取 b40 和 b50 系数
    b40_coeff = mai_get_b40_coeff(acc)
    b50_coeff = mai_get_b50_coeff(acc)

    # 计算 Rating
    rating_b40 = int(b40_coeff * decimal * acc / 100)  # 使用 b40 系数
    rating_b50 = int(b50_coeff * decimal * acc / 100)  # 使用 b50 系数

    return rating_b40, rating_b50


def linear_interpolate(x1, x2, y1, y2, x):
    """线性插值(用于计算中二游戏中的Rating)"""
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def chunithm_ra_calculate(ds: float, achievement: int):
    """计算中二游戏中指定定数谱面对应成绩的Rating结果，传入的定数格式类似15.0，传入的成绩（达成率）格式类似1010000，返回的结果是一个浮点数，即Rating"""
    if achievement <= 500000:
        calculated_rating = 0
    elif achievement < 800000:
        calculated_rating = max(
            0, linear_interpolate(500000, 800000, ds - 5, 0, achievement)
        )
    elif achievement < 900000:
        calculated_rating = max(
            0, linear_interpolate(800000, 900000, ds - 5, ds - 5, achievement)
        )
    elif achievement < 925000:
        calculated_rating = max(
            0, linear_interpolate(900000, 925000, ds - 5, ds - 3, achievement)
        )
    elif achievement < 975000:
        calculated_rating = max(
            0, linear_interpolate(925000, 975000, ds - 3, ds, achievement)
        )
    elif achievement < 1000000:
        calculated_rating = ds + (achievement - 975000) // 250 * 0.01
    elif achievement < 1005000:
        calculated_rating = ds + 1.0 + (achievement - 1000000) // 100 * 0.01
    elif achievement < 1007500:
        calculated_rating = ds + 1.5 + (achievement - 1005000) // 50 * 0.01
    elif achievement < 1009000:
        calculated_rating = ds + 2.0 + (achievement - 1007500) // 100 * 0.01
    else:
        calculated_rating = ds + 2.15

    return calculated_rating


def deduplicate(query_result):
    """
    根据 ObjectId 对 MongoDB 查询结果进行去重。

    :param query_result: MongoDB 查询返回的文档列表（如 cursor 或 list）
    :return: 去重后的文档列表
    """
    seen = set()
    unique_results = []

    for document in query_result:
        object_id = document.get("_id")
        if object_id and object_id not in seen:
            seen.add(object_id)
            unique_results.append(document)

    return unique_results


def format_timedelta(td: timedelta) -> str:
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days} 天 {hours} 小时 {minutes} 分钟"


def check_level(level: str):
    if level in [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "7+",
        "8",
        "8+",
        "9",
        "9+",
        "10",
        "10+",
        "11",
        "11+",
        "12",
        "12+",
        "13",
        "13+",
        "14",
        "14+",
        "15",
        "15+",
    ]:
        return True
    return False


def split_plate_name(plate_name: str):
    # 定义正则表达式，匹配以“将”、“极”、“神”或“舞舞”结尾的名词
    pattern = r"^(.*?)(将|极|神|舞舞)$"
    match = re.match(pattern, plate_name)

    if match:
        # 如果匹配成功，返回拆分后的两部分
        return match.group(1), match.group(2)
    else:
        # 如果匹配失败，返回None
        return None


async def get_instance_qid(bot: Bot):
    # 从缓存中尝试获取QQ号
    res = global_cache.get("instance_qid")
    if res:
        return res
    instance = await bot.get_login_info()
    qid = instance["user_id"]
    nickname = instance["nickname"]
    global_cache.set("instance_qid", qid)
    global_cache.set("instace_nickname", nickname)
    return qid
