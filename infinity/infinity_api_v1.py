import json

import PIL.Image
import httpx

from infinity import (
    get_qq_groups_joined_count,
    get_memory_usage,
    get_message_count_last_hour,
    get_hourly_message_processed,
    get_running_time,
    format_timedelta,
    check_diving_fish,
    check_fanyu,
    check_lxns,
    check_wahlap,
    CacheManager,
    connection,
    MaiDifficulty,
    check_level,
    maimai_ra_calculate,
    split_plate_name,
    ChuniDifficulty,
    chunithm_ra_calculate,
)
from infinity.chunithm_previewer_v1 import get_chunithm_preview_v1
from infinity.image_v2 import (
    maimai_song_card_img,
    generate_maimai_filename,
    get_maimai_shortest_song_id,
    chunithm_song_card_img,
    generate_chunithm_filename,
)
from infinity.maimai_lib_v1.mai_best_50 import mai_best50
from infinity.maimai_lib_v1.mai_lv_score import song_data_filter, draw_mai_lv
from infinity.maimai_lib_v1.mai_plate_completion import draw_user_music_info
from infinity.maimai_lib_v1.mai_score import generate_tool, mai_score
from infinity.maimai_lib_v1.music import plate_process_xray
from infinity.maimai_lib_v1.request_client import get_player_records
from infinity.maimai_lib_v1.score_line import score_line
from infinity.maimai_lib_v1.tool import translate_df_to_lx, filter_all_perfect_records
from infinity.model.maimai_version import MaiVersion
from infinity.model.uni_message import create_infinity_message, InfinityUniMessage
from nonebot.adapters.onebot.v11 import Bot as OnebotV11Bot

from infinity.userdata_client_v2 import LxnsClient
from infinity.whitelist import (
    add_whitelist_qq_group,
    remove_whitelist_qq_group,
    add_banned_qq_user,
)

msg_cache = CacheManager("message", 256)


async def inf_hello_world():
    """
    构建一个包含Hello, World!字符串的消息模型
    """
    msg = create_infinity_message().add_content("Hello, World!")
    return msg


async def inf_ping(bot: OnebotV11Bot, is_admin: bool = False):
    """
    构建一个包含Ping字符串的消息模型
    """
    memory_usage = get_memory_usage()
    msg = create_infinity_message().add_content("Ciallo～(∠・ω< )⌒☆")
    msg.add_content(f"已加入群组数：{await get_qq_groups_joined_count(bot)}")
    msg.add_content(f"当前内存占用：{memory_usage[3]}% | {memory_usage[4]}%")
    if is_admin:
        msg.add_content(f"Diving-Fish：{'好' if await check_diving_fish() else '坏'}")
        msg.add_content(f"落雪咖啡屋：{'好' if await check_lxns() else '坏'}")
        msg.add_content(f"Xray Bot 数据库：{'好' if await check_fanyu() else '坏'}")
        msg.add_content(f"华立API：{'好' if await check_wahlap() else '坏'}")
    msg.add_content(f"近一小时处理消息：{get_message_count_last_hour()} 条")
    msg.add_content(
        f"平均每小时处理消息：{round(get_hourly_message_processed(), 2)} 条"
    )
    msg.add_content(f"服务器已运行：{format_timedelta(get_running_time())}")
    return msg


async def inf_help():
    """
    构建一个包含帮助信息的消息模型
    """
    help_img = PIL.Image.open("assets/img/help-infinity.png")
    msg = create_infinity_message().add_image(help_img)
    return msg


async def inf_add_whitelist_qq_group(group_id: int):
    """
    将指定QQ群加入白名单
    """
    msg = create_infinity_message()
    add_whitelist_qq_group(group_id)
    msg.add_content(f"群 {group_id} 开启成功。")
    return msg


async def inf_remove_whitelist_qq_group(group_id: int):
    """
    将指定QQ群移出白名单
    """
    msg = create_infinity_message()
    remove_whitelist_qq_group(group_id)
    msg.add_content(f"群 {group_id} 关闭成功。")
    return msg


async def inf_ban_qq_user(user_id: int):
    """
    拉黑指定QQ用户
    """
    msg = create_infinity_message()
    add_banned_qq_user(user_id)
    msg.add_content(f"用户 {user_id} 拉黑成功。")
    return msg


async def inf_unban_qq_user(user_id: int):
    """
    解黑指定QQ用户
    """
    msg = create_infinity_message()
    add_banned_qq_user(user_id)
    msg.add_content(f"用户 {user_id} 解黑成功。")
    return msg


async def inf_muted(group_id: int, group_name: str, operator_id: int):
    """
    生成一个被禁言通知消息
    """
    msg = create_infinity_message()
    msg.add_content(f"在群组 {group_id} 被管理员 {operator_id} 禁言了！")
    msg.add_content(f"群聊名称：{group_name}")
    return msg


async def inf_kicked(group_id: int):
    """
    生成一个被踢出通知消息
    """
    msg = create_infinity_message()
    msg.add_content(f"在群组 {group_id} 被踢出了！")
    return msg


async def inf_find_tippy(group_id: int, group_name: str):
    """
    生成一个发现Tippy的消息
    """
    msg = create_infinity_message()
    msg.add_content(f"因神秘力量自动退出了群组 {group_id}。")
    msg.add_content(f"群聊名称：{group_name}")
    return msg


async def inf_update_required():
    """
    生成一个需要更新的消息
    """
    msg = create_infinity_message()
    msg.add_content("已收到请求，准备更新乐曲数据。")
    return msg


async def inf_update_completed(ok: bool = True):
    """
    生成一个更新完成的消息
    """
    msg = create_infinity_message()
    if ok:
        msg.add_content("乐曲数据更新完成。")
    else:
        msg.add_content("更新乐曲数据失败，请检查控制台输出。")
    return msg


async def inf_mai_help():
    """
    生成一个mai插件帮助消息
    """
    msg = create_infinity_message()
    msg.add_content("此指令用于「舞萌DX」游戏相关功能。")
    msg.add_content("此功能的使用说明请查看功能使用文档。")
    msg.add_content(
        "https://docs.qq.com/aio/p/scm9oh4ypvgb8cq?p=GTjZy8z9ljU8DTngs7AY3wc"
    )
    return msg


async def gen_mai_music_card(msg: InfinityUniMessage, music_id: int):
    # 生成图片
    img = await maimai_song_card_img(music_id)
    if img:
        msg.success()
        msg.add_image(img)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def gen_mai_music_text(msg: InfinityUniMessage, music_id: int):
    # 生成文字信息
    # 获取封面
    cover = PIL.Image.open(
        f"./assets/cover/mai/{generate_maimai_filename(get_maimai_shortest_song_id(music_id))}"
    )
    msg.add_image(cover)
    # 根据信息生成文本
    music_detail = await connection.query_maimai_song_by_id(
        get_maimai_shortest_song_id(music_id) if music_id <= 100000 else music_id
    )
    if music_detail:
        is_dx = music_id > 10000
        if is_dx:
            levels_str = ", ".join([chart.level for chart in music_detail.dx_charts])
            decimal_str = ", ".join(
                [str(chart.level_value) for chart in music_detail.dx_charts]
            )
        else:
            levels_str = ", ".join([chart.level for chart in music_detail.sd_charts])
            decimal_str = ", ".join(
                [str(chart.level_value) for chart in music_detail.sd_charts]
            )
        msg.success()
        msg.add_content(str(music_id) + ". " + music_detail.title)
        msg.add_content("艺术家：" + music_detail.artist)
        msg.add_content("分类：" + music_detail.genre_cn)
        msg.add_content("BPM：" + str(music_detail.bpm))
        msg.add_content("谱面类型：DX" if is_dx else "谱面类型：标准")
        msg.add_content("版本：" + music_detail.version_name)
        msg.add_content("等级：" + levels_str)
        msg.add_content("定数：" + decimal_str)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def gen_mai_chart_text(
    msg: InfinityUniMessage, difficulty: MaiDifficulty, music_id: int
):
    """
    生成舞萌谱面信息
    """
    # 生成文字信息
    # 获取封面
    try:
        cover = PIL.Image.open(
            f"./assets/cover/mai/{generate_maimai_filename(get_maimai_shortest_song_id(music_id))}"
        )
    except FileNotFoundError:
        # 歌曲不存在
        msg.add_content("歌曲不存在哦！")
        return msg
    msg.add_image(cover)
    # 根据信息生成文本
    music_detail = await connection.query_maimai_song_by_id(
        get_maimai_shortest_song_id(music_id) if music_id <= 100000 else music_id
    )
    if music_detail:
        is_dx = music_id > 10000
        if (
            is_dx
            and len(music_detail.dx_charts) >= difficulty.int() + 1
            and difficulty.int() != -1
        ):
            # 难度存在，获取其信息
            chart = music_detail.dx_charts[difficulty.int()]
        elif (
            not is_dx
            and len(music_detail.sd_charts) >= difficulty.int() + 1
            and difficulty.int() != -1
        ):
            # 难度存在，获取其信息
            chart = music_detail.sd_charts[difficulty.int()]
        else:
            msg.add_content("指定的难度不对哦！")
            return msg
        msg.success()
        msg.add_content(str(music_id) + ". " + music_detail.title)
        msg.add_content("谱面类型：DX" if is_dx else "谱面类型：标准")
        msg.add_content("BPM：" + str(music_detail.bpm))
        msg.add_content(
            f"难度：{difficulty.str()} {chart.level}（{chart.level_value}）"
        )
        msg.add_content("TOTAL：" + str(chart.notes.total))
        msg.add_content("TAP：" + str(chart.notes.taps))
        msg.add_content("HOLD：" + str(chart.notes.holds))
        msg.add_content("SLIDE：" + str(chart.notes.slides))
        msg.add_content("BREAK：" + str(chart.notes.breaks))
        if is_dx:
            msg.add_content("TOUCH：" + str(chart.notes.touchs))
        msg.add_content("谱师：" + chart.note_designer)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def inf_mai_id(music_id: int):
    """
    基于歌曲id查询歌曲信息（图片版）
    """
    msg = create_infinity_message()
    msg = await gen_mai_music_card(msg, music_id)
    return msg


async def inf_mai_song(music_id: int):
    """
    基于歌曲id查询歌曲信息（文字版）
    """
    msg = create_infinity_message()
    msg = await gen_mai_music_text(msg, music_id)
    return msg


async def inf_mai_chart(difficulty: str, music_id: int):
    """
    基于难度和歌曲id查询谱面信息
    """
    msg = create_infinity_message()
    difficulty = MaiDifficulty(difficulty)
    msg = await gen_mai_chart_text(msg, difficulty, music_id)
    return msg


async def inf_mai_chage(keyword: str):
    """
    基于关键字查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_keyword(keyword)
    if len(music_list) == 0:
        # 如果没有搜索到结果，通过别名再次搜索
        alias_list = await connection.query_maimai_song_by_alias(keyword)
        if len(alias_list) == 0:
            msg.add_content("没有搜索到任何结果。")
        elif len(alias_list) == 1:
            # 获取歌曲信息
            msg = await gen_mai_music_card(msg, alias_list[0])
        elif len(alias_list) > 1:
            msg.enable_paging()
            msg.success()
            for music_id in alias_list:
                music_detail = await connection.query_maimai_song_by_id(
                    get_maimai_shortest_song_id(music_id)
                    if music_id <= 100000
                    else music_id
                )
                if music_detail:
                    msg.add_content(f"{music_id}  {music_detail.title}")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_mai_search(keyword: str):
    """
    基于关键字查询歌曲信息，不进行别名匹配
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_keyword(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_mai_what_song(keyword: str):
    """
    基于别名查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_alias(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0])
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music_id in music_list:
            music_detail = await connection.query_maimai_song_by_id(
                get_maimai_shortest_song_id(music_id)
                if music_id <= 100000
                else music_id
            )
            if music_detail:
                msg.add_content(f"{music_id}  {music_detail.title}")
    return msg


async def inf_mai_artist(keyword: str):
    """
    基于艺术家查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_artist(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_mai_bpm(bpm: int):
    """
    基于BPM查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_bpm(bpm)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_mai_decimal(difficulty: str, decimal: float):
    """
    基于定数查询歌曲信息
    """
    msg = create_infinity_message()
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = MaiDifficulty(difficulty)
    else:
        difficulty = MaiDifficulty(-1)
    music_list = await connection.query_maimai_song_by_decimal_and_difficulty(
        decimal, difficulty
    )
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            # 检查其具体谱面信息
            for chart in music.dx_charts if music.id > 10000 else music.sd_charts:
                if chart.level_value == decimal and (
                    difficulty.int() == -1 or chart.difficulty == difficulty.int()
                ):
                    msg.add_content(
                        f"{music.id} {MaiDifficulty(chart.difficulty).str()} {music.title}"
                    )
    return msg


async def inf_mai_level(difficulty: str, level: str):
    """
    基于等级查询歌曲信息
    """
    msg = create_infinity_message()
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = MaiDifficulty(difficulty)
    else:
        difficulty = MaiDifficulty(-1)
    music_list = await connection.query_maimai_song_by_level_and_difficulty(
        level, difficulty
    )
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            # 检查其具体谱面信息
            for chart in music.dx_charts if music.id > 10000 else music.sd_charts:
                if chart.level == level and (
                    difficulty.int() == -1 or chart.difficulty == difficulty.int()
                ):
                    msg.add_content(
                        f"{music.id} {MaiDifficulty(chart.difficulty).str()} {music.title}"
                    )
    return msg


async def inf_mai_total(total_notes: int):
    """
    基于物量查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_maimai_song_by_total_notes(total_notes)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_mai_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_mai_seek_aliases(music_id: int):
    """
    查询歌曲别名
    """
    msg = create_infinity_message()
    # 先查歌曲是否存在
    music_detail = await connection.query_maimai_song_by_id(
        get_maimai_shortest_song_id(music_id) if music_id <= 100000 else music_id
    )
    if music_detail:
        msg.set_suffix("\n别名数据来自 Xray Bot。")
        alias_list = await connection.query_maimai_aliases_by_id(music_id)
        if len(alias_list) == 0:
            msg.add_content("这首歌还没有别名。")
        else:
            msg.add_content("这首歌的别名有: ")
            for music_alias in alias_list:
                msg.add_content(music_alias)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def inf_mai_roll():
    """
    随机查询歌曲信息
    """
    msg = create_infinity_message()
    music = await connection.roll_maimai_song()
    if music:
        music_id = music.id
        msg = await gen_mai_music_card(msg, music_id)
    return msg


async def inf_mai_roll_by_decimal(difficulty: str, decimal: float):
    """
    指定定数查询随机歌曲信息
    """
    msg = create_infinity_message()
    if not isinstance(decimal, float) or (decimal < 1.0 or decimal > 15.0):
        msg.add_content("提供的信息不对哦！")
        return msg
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = MaiDifficulty(difficulty)
        if difficulty.int() == -1:
            msg.add_content("提供的信息不对哦！")
            return msg
    else:
        difficulty = MaiDifficulty(-1)
    music = await connection.roll_maimai_song_by_decimal_and_difficulty(
        decimal, difficulty
    )
    if music:
        music_id = music.id
        msg = await gen_mai_music_card(msg, music_id)
    else:
        msg.add_content("指定的条件下没有谱面。")
    return msg


async def inf_mai_roll_by_level(difficulty: str, level: str):
    """
    指定等级查询随机歌曲信息
    """
    msg = create_infinity_message()
    if not check_level(level):
        msg.add_content("提供的信息不对哦！")
        return msg
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = MaiDifficulty(difficulty)
        if difficulty.int() == -1:
            msg.add_content("提供的信息不对哦！")
            return msg
    else:
        difficulty = MaiDifficulty(-1)
    music = await connection.roll_maimai_song_by_level_and_difficulty(level, difficulty)
    if music:
        music_id = music.id
        msg = await gen_mai_music_card(msg, music_id)
    return msg


async def inf_mai_plate_song_list_v1(version_name: str):
    msg = create_infinity_message()
    version_kanji = MaiVersion(version_name).kanji
    if version_kanji:
        # 生成图片
        img = await draw_user_music_info(version_kanji, "将", user_name="")
        msg.success()
        msg.add_image(img)
    else:
        msg.add_content("没有这个版本哦！")
    return msg


async def inf_mai_plate_requirement():
    msg = create_infinity_message()
    img = PIL.Image.open("./assets/img/plate-requirement.jpg")
    msg.add_image(img)
    return msg


async def inf_mai_ra_calculating(decimal: float, acc: float):
    msg = create_infinity_message()
    if not isinstance(decimal, float) or (decimal < 1.0 or decimal > 15.0):
        msg.add_content("提供的信息不对哦！")
        msg.add_content("使用方法：/mai ra计算 定数 达成率")
        return msg
    if not isinstance(acc, float) or (acc < 0.0 or acc > 101.0):
        msg.add_content("提供的信息不对哦！")
        msg.add_content("使用方法：/mai ra计算 定数 达成率")
        return msg
    # 计算ra
    ra = maimai_ra_calculate(decimal, acc)
    msg.add_content(f"定数 {decimal:.1f}")
    msg.add_content(f"在 {acc:.4f}% 的得分是 {ra[1]} 。")
    return msg


async def inf_mai_score_line_v1(difficulty: str, music_id: int):
    msg = create_infinity_message()
    mai_difficulty = MaiDifficulty(difficulty)
    if difficulty and mai_difficulty == "-1":
        msg.add_content("提供的难度不对哦！")
        return msg
    try:
        img = await score_line(str(music_id), mai_difficulty.int())
        if img:
            msg.success()
            msg.add_image(img)
    except TypeError:
        msg.add_content("歌曲不存在哦！")
    return msg


async def inf_mai_course():
    msg = create_infinity_message()
    img = PIL.Image.open("./assets/img/mai-course.png")
    msg.add_image(img)
    return msg


async def inf_mai_shincourse():
    msg = create_infinity_message()
    img = PIL.Image.open("./assets/img/mai-shincourse.png")
    msg.add_image(img)
    return msg


async def inf_mai_random_course():
    pass


async def inf_mai_otomodachi():
    pass


async def inf_mai_find_arcade(keyword: str):
    msg = create_infinity_message()
    arcade = await connection.query_maimai_arcade_by_keyword(keyword)
    pass


async def inf_mai_b50_v1(
    username: str = "", qq: str = "", is_lxns: bool = False, friend_code: str = ""
):
    """
    生成Best 50图片
    """
    msg = create_infinity_message()
    if is_lxns:
        if friend_code == "":
            msg.add_content("未提供好友码！")
            return msg
        lx_client = LxnsClient()
        best_data = await lx_client.get(f"maimai/player/{friend_code}/bests")
        lx_data_v = best_data.json()
        player_data = await lx_client.get(f"maimai/player/{friend_code}")
        if player_data.status_code != 200:
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        player_data = player_data.json()
        other_data = [
            player_data["data"]["name"],
            {"name": "maimai DX Rating Information", "color": "Normal"},
            player_data["data"]["course_rank"],
            0,
        ]
    else:
        if username == "" and qq == "":
            msg.add_content("用户名和QQ号均未提供。")
            return msg
        payload = {"b50": 1}
        if username:
            payload["username"] = username
        else:
            payload["qq"] = qq
        req = httpx.post(
            "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload
        )
        if req.status_code != 200:
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        player_data = req.json()
        lx_data_v = {"data": {}}
        try:
            standard_total = sum([score["ra"] for score in player_data["charts"]["sd"]])
            dx_total = sum([score["ra"] for score in player_data["charts"]["dx"]])
        except Exception as e:
            msg.set_exception(e.__str__())
            return msg
        lx_data_v["data"]["standard_total"] = standard_total
        lx_data_v["data"]["dx_total"] = dx_total
        lx_data_v["data"]["standard"] = translate_df_to_lx(player_data["charts"]["sd"])
        lx_data_v["data"]["dx"] = translate_df_to_lx(player_data["charts"]["dx"])
        course_rank = player_data["additional_rating"]
        if course_rank >= 11:
            course_rank = player_data["additional_rating"] + 1
        other_data = [
            player_data["nickname"],
            {"name": "maimai DX Rating Information", "color": "Normal"},
            course_rank,
            0,
            {"name": player_data["plate"]},
            None,
            None,
        ]
    # noinspection PyTypeChecker
    # 蘑菇头的代码我真的看不懂，我也不知道为什么这为什么能跑起来，总之看见标黄难受
    img_data = mai_best50.lxns(lx_data_v["data"], player_data=other_data)
    msg.success()
    msg.add_image(img_data)
    return msg


async def inf_mai_ap50_v1(
    username: str = "", qq: str = "", is_lxns: bool = False, friend_code: str = ""
):
    """
    生成AP Best 50图片
    """
    msg = create_infinity_message()
    if is_lxns:
        # 日后重置数据获取相关函数之后再解决
        msg.add_content("暂时不支持从落雪咖啡屋获取AP50数据！")
        return msg
    else:
        if username == "" and qq == "":
            msg.add_content("用户名和QQ号均未提供。")
            return msg
        payload = {"b50": 1}
        payload_rec = {}
        if username:
            payload["username"] = username
            payload_rec["username"] = username
        else:
            payload["qq"] = qq
            payload_rec["qq"] = qq
        req = httpx.post(
            "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload
        )
        if req.status_code != 200:
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        player_b50_data = req.json()
        # 获取玩家B50信息以获取基础信息
        player_records_data = await get_player_records(payload_rec)
        match player_records_data:
            case "Player Not Found":
                msg.add_content("查询的用户不存在或设置了隐私。")
                return msg
            case "Private Setting":
                msg.add_content("查询的用户不存在或设置了隐私。")
                return msg
            case "Data Lost":
                msg.set_exception("数据丢失。")
            case _:
                pass
            # 获取玩家所有成绩信息准备过滤

        ap_b35_data, ap_b15_data = filter_all_perfect_records(
            player_records_data["records"]
        )
        if len(ap_b35_data) == 0 and len(ap_b15_data) == 0:
            msg.add_content("您还没有AP的成绩哦，请继续加油！")
            return msg
        player_data = {
            "additional_rating": player_b50_data["additional_rating"],
            "charts": {"dx": ap_b15_data, "sd": ap_b35_data},
            "nickname": player_b50_data["nickname"],
            "plate": player_b50_data["plate"],
            "rating": player_b50_data["rating"],
            "user_general_data": player_b50_data["user_general_data"],
            "username": player_b50_data["username"],
        }
        lx_data_v = {"data": {}}
        try:
            standard_total = sum([score["ra"] for score in player_data["charts"]["sd"]])
            dx_total = sum([score["ra"] for score in player_data["charts"]["dx"]])
        except Exception as e:
            msg.set_exception(e.__str__())
            return msg
        lx_data_v["data"]["standard_total"] = standard_total
        lx_data_v["data"]["dx_total"] = dx_total
        lx_data_v["data"]["standard"] = translate_df_to_lx(player_data["charts"]["sd"])
        lx_data_v["data"]["dx"] = translate_df_to_lx(player_data["charts"]["dx"])
        course_rank = player_data["additional_rating"]
        if course_rank >= 11:
            course_rank = player_data["additional_rating"] + 1
        other_data = [
            player_data["nickname"],
            {"name": "maimai DX Rating Information", "color": "Normal"},
            course_rank,
            0,
            {"name": player_data["plate"]},
            None,
            None,
        ]
    # noinspection PyTypeChecker
    # 蘑菇头的代码我真的看不懂，我也不知道为什么这为什么能跑起来，总之看见标黄难受
    img_data = mai_best50.lxns(lx_data_v["data"], player_data=other_data)
    msg.success()
    msg.add_image(img_data)
    return msg


async def inf_mai_plate_completion_v1(qq: int = "", plate_name: str = ""):
    msg = create_infinity_message()
    if plate_name == "真将":
        msg.add_content("不存在这个牌子！")
    if plate_name == "霸者":
        version_name = "霸"
        plate_mode = "者"
    else:
        version_name, plate_mode = split_plate_name(plate_name)
    version_kanji = MaiVersion(version_name).kanji if version_name != "霸" else "霸"
    if version_kanji:
        # 生成图片
        img = await draw_user_music_info(version_kanji, plate_mode, qq=qq)
        msg.success()
        msg.add_image(img)
    else:
        msg.add_content("没有这个版本哦！")
    return msg


async def inf_mai_plate_process_v1(qq: str = "", plate_name: str = ""):
    msg = create_infinity_message()
    if plate_name == "真将":
        msg.add_content("不存在这个牌子！")
    if plate_name == "霸者":
        version_name = "霸"
        plate_mode = "者"
    else:
        version_name, plate_mode = split_plate_name(plate_name)
    data = plate_process_xray(version_name, qq, plate_mode, version_name)
    msg.add_content(data)
    return msg


async def inf_mai_level_score_list_v1(qq: str = "", level: str = "", page: int = 1):
    msg = create_infinity_message()
    if not check_level(level):
        msg.add_content("提供的信息不对哦！")
        return msg
    with open("./assets/data/maidxCN-Today.json", "r", encoding="utf-8") as f:
        music_data = json.load(f)

    get_status = await get_player_records({"qq": qq})
    match get_status:
        case "Player Not Found":
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        case "Private Setting":
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        case "Data Lost":
            msg.set_exception("数据丢失。")
            return msg
        case _:
            pass

    draw_data = song_data_filter(get_status, level, page, music_data, level)
    match draw_data:
        case "Data is Empty":
            msg.add_content("您在当前难度下没有成绩。")
            return msg
        case "Page Error":
            msg.add_content("提供的信息不对哦！")
            return msg
        case _:
            pass

    img = draw_mai_lv(draw_data, music_data)
    msg.success()
    msg.add_image(img)
    return msg


async def inf_mai_score_v1(qq: str = "", music_id: str = ""):
    msg = create_infinity_message()
    with open("./assets/data/maidxCN-Today.json", "r", encoding="utf-8") as f:
        music_data = json.load(f)
    if music_id not in music_data.keys():
        msg.add_content("歌曲不存在哦！")
    elif int(music_id) >= 100000:
        msg.add_content("宴会场请通过分数列表查询。")
        # ID筛选完毕
    get_status = await get_player_records({"qq": qq})
    match get_status:
        case "Player Not Found":
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        case "Private Setting":
            msg.add_content("查询的用户不存在或设置了隐私。")
            return msg
        case "Data Lost":
            msg.set_exception("数据丢失。")
            return msg
        case _:
            pass
    # 获取用户数据

    filter_song_data = []
    for single_song_data in get_status["records"]:
        if str(single_song_data["song_id"]) == music_id:
            filter_song_data.append(single_song_data)
    if len(filter_song_data) == 0:
        msg.add_content("您没有这个歌曲的成绩哦！")
    # 过滤用户成绩
    translate_data = generate_tool.translate_fish2lx(filter_song_data)
    # noinspection PyTypeChecker
    img = mai_score.lxns(translate_data, music_data)
    msg.success()
    msg.add_image(img)
    return msg


async def inf_chu_help():
    """
    生成一个mai插件帮助消息
    """
    msg = create_infinity_message()
    msg.add_content("此指令用于「中二节奏」游戏相关功能。")
    msg.add_content("此功能的使用说明请查看功能使用文档。")
    msg.add_content(
        "https://docs.qq.com/aio/p/scm9oh4ypvgb8cq?p=GTjZy8z9ljU8DTngs7AY3wc"
    )
    return msg


async def gen_chu_music_card(msg: InfinityUniMessage, music_id: int):
    # 生成图片
    img = await chunithm_song_card_img(music_id)
    if img:
        msg.success()
        msg.add_image(img)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def gen_chu_music_text(msg: InfinityUniMessage, music_id: int):
    # 生成文字信息
    # 获取封面
    cover = PIL.Image.open(f"./assets/cover/chu/{generate_chunithm_filename(music_id)}")
    msg.add_image(cover)
    # 根据信息生成文本
    music_detail = await connection.query_chunithm_song_by_id(music_id)
    if music_detail:
        levels_str = ", ".join([chart.level for chart in music_detail.charts])
        decimal_str = ", ".join(
            [str(chart.level_value) for chart in music_detail.charts]
        )
        msg.success()
        msg.add_content(str(music_id) + ". " + music_detail.title)
        msg.add_content("艺术家：" + music_detail.artist)
        msg.add_content("分类：" + music_detail.genre)
        msg.add_content("BPM：" + str(music_detail.bpm))
        msg.add_content("版本：" + music_detail.version_name)
        msg.add_content("等级：" + levels_str)
        msg.add_content("定数：" + decimal_str)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def gen_chu_chart_text(
    msg: InfinityUniMessage, difficulty: ChuniDifficulty, music_id: int
):
    """
    生成舞萌谱面信息
    """
    # 生成文字信息
    # 获取封面
    try:
        cover = PIL.Image.open(
            f"./assets/cover/chu/{generate_chunithm_filename(music_id)}"
        )
    except FileNotFoundError:
        # 歌曲不存在
        msg.add_content("歌曲不存在哦！")
        return msg
    msg.add_image(cover)
    # 根据信息生成文本
    music_detail = await connection.query_chunithm_song_by_id(music_id)
    if music_detail:
        if len(music_detail.charts) >= difficulty.int() + 1 and difficulty.int() != -1:
            # 难度存在，获取其信息
            chart = music_detail.charts[difficulty.int()]
        else:
            msg.add_content("指定的难度不对哦！")
            return msg
        msg.success()
        msg.add_content(str(music_id) + ". " + music_detail.title)
        msg.add_content("BPM：" + str(music_detail.bpm))
        msg.add_content(
            f"难度：{difficulty.str()} {chart.level}（{chart.level_value}）"
        )
        msg.add_content("TOTAL：" + str(chart.notes.total))
        msg.add_content("TAP：" + str(chart.notes.taps))
        msg.add_content("HOLD：" + str(chart.notes.holds))
        msg.add_content("SLIDE：" + str(chart.notes.slides))
        msg.add_content("AIR：" + str(chart.notes.airs))
        msg.add_content("FLICK：" + str(chart.notes.flicks))
        msg.add_content("谱师：" + chart.note_designer)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def inf_chu_id(music_id: int):
    """
    基于歌曲id查询歌曲信息（图片版）
    """
    msg = create_infinity_message()
    msg = await gen_chu_music_card(msg, music_id)
    return msg


async def inf_chu_song(music_id: int):
    """
    基于歌曲id查询歌曲信息（文字版）
    """
    msg = create_infinity_message()
    msg = await gen_chu_music_text(msg, music_id)
    return msg


async def inf_chu_chart(difficulty: str, music_id: int):
    """
    基于难度和歌曲id查询谱面信息
    """
    msg = create_infinity_message()
    difficulty = ChuniDifficulty(difficulty)
    msg = await gen_chu_chart_text(msg, difficulty, music_id)
    return msg


async def inf_chu_chage(keyword: str):
    """
    基于关键字查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_keyword(keyword)
    if len(music_list) == 0:
        # 如果没有搜索到结果，通过别名再次搜索
        alias_list = await connection.query_chunithm_song_by_alias(keyword)
        if len(alias_list) == 0:
            msg.add_content("没有搜索到任何结果。")
        elif len(alias_list) == 1:
            # 获取歌曲信息
            msg = await gen_chu_music_card(msg, alias_list[0])
        elif len(alias_list) > 1:
            msg.enable_paging()
            msg.success()
            for music_id in alias_list:
                music_detail = await connection.query_chunithm_song_by_id(music_id)
                if music_detail:
                    msg.add_content(f"{music_id}  {music_detail.title}")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_chu_search(keyword: str):
    """
    基于关键字查询歌曲信息，不进行别名匹配
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_keyword(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_chu_what_song(keyword: str):
    """
    基于别名查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_alias(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0])
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music_id in music_list:
            music_detail = await connection.query_chunithm_song_by_id(music_id)
            if music_detail:
                msg.add_content(f"{music_id}  {music_detail.title}")
    return msg


async def inf_chu_artist(keyword: str):
    """
    基于艺术家查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_artist(keyword)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_chu_bpm(bpm: int):
    """
    基于BPM查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_bpm(bpm)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_chu_decimal(difficulty: str, decimal: float):
    """
    基于定数查询歌曲信息
    """
    msg = create_infinity_message()
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = ChuniDifficulty(difficulty)
    else:
        difficulty = ChuniDifficulty(-1)
    music_list = await connection.query_chunithm_song_by_decimal_and_difficulty(
        decimal, difficulty
    )
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            # 检查其具体谱面信息
            for chart in music.charts:
                if chart.level_value == decimal and (
                    difficulty.int() == -1 or chart.difficulty == difficulty.int()
                ):
                    msg.add_content(
                        f"{music.id} {ChuniDifficulty(chart.difficulty).str()} {music.title}"
                    )
    return msg


async def inf_chu_level(difficulty: str, level: str):
    """
    基于等级查询歌曲信息
    """
    msg = create_infinity_message()
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = ChuniDifficulty(difficulty)
    else:
        difficulty = ChuniDifficulty(-1)
    music_list = await connection.query_chunithm_song_by_level_and_difficulty(
        level, difficulty
    )
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            # 检查其具体谱面信息
            for chart in music.charts:
                if chart.level == level and (
                    difficulty.int() == -1 or chart.difficulty == difficulty.int()
                ):
                    msg.add_content(
                        f"{music.id} {ChuniDifficulty(chart.difficulty).str()} {music.title}"
                    )
    return msg


async def inf_chu_total(total_notes: int):
    """
    基于物量查询歌曲信息
    """
    msg = create_infinity_message()
    music_list = await connection.query_chunithm_song_by_total_notes(total_notes)
    if len(music_list) == 0:
        msg.add_content("没有搜索到任何结果。")
    elif len(music_list) == 1:
        msg = await gen_chu_music_card(msg, music_list[0].id)
    elif len(music_list) > 1:
        msg.enable_paging()
        msg.success()
        for music in music_list:
            msg.add_content(f"{music.id}  {music.title}")
    return msg


async def inf_chu_seek_aliases(music_id: int):
    """
    查询歌曲别名
    """
    msg = create_infinity_message()
    # 先查歌曲是否存在
    music_detail = await connection.query_chunithm_song_by_id(music_id)
    if music_detail:
        msg.set_suffix("\n别名数据来自 Xray Bot。")
        alias_list = await connection.query_chunithm_aliases_by_id(music_id)
        if len(alias_list) == 0:
            msg.add_content("这首歌还没有别名。")
        else:
            msg.add_content("这首歌的别名有: ")
            for music_alias in alias_list:
                msg.add_content(music_alias)
    else:
        msg.add_content("歌曲不存在哦！")
    return msg


async def inf_chu_roll():
    """
    随机查询歌曲信息
    """
    msg = create_infinity_message()
    music = await connection.roll_chunithm_song()
    if music:
        music_id = music.id
        msg = await gen_chu_music_card(msg, music_id)
    return msg


async def inf_chu_roll_by_decimal(difficulty: str, decimal: float):
    """
    指定定数查询随机歌曲信息
    """
    msg = create_infinity_message()
    if not isinstance(decimal, float) or (decimal < 1.0 or decimal > 15.0):
        msg.add_content("提供的信息不对哦！")
        return msg
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = ChuniDifficulty(difficulty)
        if difficulty.int() == -1:
            msg.add_content("提供的信息不对哦！")
            return msg
    else:
        difficulty = ChuniDifficulty(-1)
    music = await connection.roll_chunithm_song_by_decimal_and_difficulty(
        decimal, difficulty
    )
    if music:
        music_id = music.id
        msg = await gen_chu_music_card(msg, music_id)
    else:
        msg.add_content("指定的条件下没有谱面。")
    return msg


async def inf_chu_roll_by_level(difficulty: str, level: str):
    """
    指定等级查询随机歌曲信息
    """
    msg = create_infinity_message()
    if not check_level(level):
        msg.add_content("提供的信息不对哦！")
        return msg
    is_difficulty = False
    if difficulty != "":
        is_difficulty = True
    if is_difficulty:
        difficulty = ChuniDifficulty(difficulty)
        if difficulty.int() == -1:
            msg.add_content("提供的信息不对哦！")
            return msg
    else:
        difficulty = ChuniDifficulty(-1)
    music = await connection.roll_chunithm_song_by_level_and_difficulty(
        level, difficulty
    )
    if music:
        music_id = music.id
        msg = await gen_chu_music_card(msg, music_id)
    return msg


async def inf_chu_ra_calculating(decimal: float, acc: float):
    msg = create_infinity_message()
    if not isinstance(decimal, float) or (decimal < 1.0 or decimal > 15.0):
        msg.add_content("提供的信息不对哦！")
        msg.add_content("使用方法：/chu ra计算 定数 达成率")
        return msg
    if not isinstance(acc, float) or (acc < 0.0 or acc > 101.0):
        msg.add_content("提供的信息不对哦！")
        msg.add_content("使用方法：/chu ra计算 定数 达成率")
        return msg
    # 计算ra
    ra = chunithm_ra_calculate(decimal, acc)
    msg.add_content(f"定数 {decimal:.1f}")
    msg.add_content(f"在 {acc:.4f}% 的得分是 {ra[1]} 。")
    return msg

async def inf_chu_chart_preview(music_id: int, difficulty: str):
    print(difficulty)
    msg = create_infinity_message()
    is_difficulty = False
    if difficulty:
        is_difficulty = True
    if is_difficulty:
        difficulty = ChuniDifficulty(difficulty)
        if difficulty.int() == -1:
            msg.add_content("提供的信息不对哦！")
            return msg
    else:
        difficulty = ChuniDifficulty(3)
    img = await get_chunithm_preview_v1(music_id, difficulty)
    if img:
        msg.success()
        msg.add_image(img)
        msg.add_content("谱面预览数据来自 sdvx.in")
    else:
        msg.add_content("您指定的谱面没有谱面预览。")
    return msg