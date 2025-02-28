from arclet.alconna import Arparma, Option
from nonebot import on_notice, get_driver
from nonebot.adapters.onebot.v11 import GroupBanNoticeEvent, GroupDecreaseNoticeEvent, GroupMessageEvent, \
    PrivateMessageEvent, Bot, MessageSegment
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna, Match, Alconna, Args, Subcommand

from infinity import check_level, message_occurred
from infinity.infinity_api_v1 import inf_mai_help, inf_mai_id, inf_mai_song, inf_mai_chart, inf_mai_chage, \
    inf_mai_what_song, inf_mai_search, inf_mai_artist, inf_mai_bpm, inf_mai_decimal, inf_mai_total, inf_mai_level, \
    inf_mai_seek_aliases, inf_mai_roll, inf_mai_roll_by_decimal, inf_mai_roll_by_level, inf_mai_plate_song_list_v1, \
    inf_mai_plate_requirement, inf_mai_ra_calculating, inf_mai_score_line_v1, inf_mai_course, inf_mai_shincourse, \
    inf_mai_b50_v1, inf_mai_ap50_v1, inf_mai_plate_completion_v1, inf_mai_plate_process_v1, inf_mai_level_score_list_v1, \
    inf_mai_score_v1
from infinity.rules import is_allowed

# noinspection PyTypeChecker
mai_command = on_alconna(
    Alconna(
    "mai",
        Subcommand(
            "help"
        ),
        Subcommand(
            "id",
            Args["music_id", int]
        ),
        Subcommand(
            "song",
            Args["music_id", int]
        ),
        Subcommand(
            "chart",
            Args["music_id", int]["difficulty", str]
        ),
        Subcommand(
            "查歌",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "search",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "曲师查歌",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1),
            alias=["艺术家查歌", "artist"]
        ),
        Subcommand(
            "BPM查歌",
            Args["bpm", int],
            Option("-p|--page", Args["page", int], default=1),
            alias=["bpm查歌", "bpm"]
        ),
        Subcommand(
            "定数查歌",
            Args["decimal", float]["difficulty?", str],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "等级查歌",
            Args["level", str]["difficulty?", str],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "物量查歌",
            Args["total_notes", int],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "查看别名",
            Args["music_id", int],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "随歌",
            alias=["random"]
        ),
        Subcommand(
            "定数随歌",
            Args["decimal", float]["difficulty?", str]
        ),
        Subcommand(
            "等级随歌",
            Args["level", str]["difficulty?", str]
        ),
        Subcommand(
            "定数表",
            Args["level", str]
        ),
        Subcommand(
            "牌子条件"
        ),
        Subcommand(
            "ra计算",
            Args["decimal", float]["acc", float]
        ),
        Subcommand(
            "分数线",
            Args["music_id", int]["difficulty?", str]
        ),
        Subcommand(
            "段位认定"
        ),
        Subcommand(
            "真段位认定"
        ),
        Subcommand(
            "随机段位认定",
            Args["type?", str]
        ),
        Subcommand(
            "友人对战"
        ),
        Subcommand(
            "查找机厅",
            Args["keyword", str]
        ),
        Subcommand(
            "b50",
            Args["username?", str],
            Option("--lxns|-lx|-lxns", Args["friend_code", str])
        ),
        Subcommand(
            "ap50",
            Args["username?", str],
            Option("--lxns|-lx|-lxns", Args["friend_code", str])
        ),

        Subcommand(
            "等级进度",
            Args["level", str]["flag", str]
        ),
        Subcommand(
            "分数列表",
            Args["level", str],
            Option("-p|--page", Args["page", int], default=1)
        ),
        Subcommand(
            "score",
            Args["music_id", str]
        ),
    ),
    use_cmd_start=True,
    use_cmd_sep=True,
    rule=is_allowed
)

# noinspection PyTypeChecker
what_song_cmd = on_alconna(
    Alconna(
        "mai {keyword:str}是什么歌",
        Option("-p|--page", Args["page", int], default=1)
    ),
    use_cmd_start=True, rule=is_allowed
)

# noinspection PyTypeChecker
version_song_list_cmd = on_alconna(
    Alconna(
        "mai {version:str}歌曲表"
    ),
    use_cmd_start=True, rule=is_allowed
)

level_and_plate_completion_cmd = on_alconna(
    Alconna(
        "mai {keyword:str}完成表"
    ),
    use_cmd_start=True, rule=is_allowed
)

level_process_cmd = on_alconna(
    Alconna(
        "mai {keyword:str}进度"
    ),
    use_cmd_start=True, rule=is_allowed
)

@mai_command.handle()
async def  _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    # 命令mai help
    message_occurred()
    if result.find("help"):
        m = await inf_mai_help()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai id
    elif result.find("id"):
        message_occurred()
        m = await inf_mai_id(result.query[int]("id.music_id"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai song
    if result.find("song"):
        message_occurred()
        m = await inf_mai_song(result.query[int]("song.music_id"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()) + MessageSegment.text(m.build()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai chart
    if result.find("chart"):
        message_occurred()
        m = await inf_mai_chart(result.query[str]("chart.difficulty"), result.query[int]("chart.music_id"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()) + MessageSegment.text(m.build()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 查歌
    if result.find("查歌"):
        message_occurred()
        m = await inf_mai_chage(result.query[str]("查歌.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("查歌.page"):
                    page = result.query[int]("查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai search
    if result.find("search"):
        message_occurred()
        m = await inf_mai_search(result.query[str]("search.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("search.page"):
                    page = result.query[int]("search.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 曲师查歌
    if result.find("曲师查歌"):
        message_occurred()
        m = await inf_mai_artist(result.query[str]("曲师查歌.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("曲师查歌.page"):
                    page = result.query[int]("曲师查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai BPM查歌
    if result.find("BPM查歌"):
        message_occurred()
        m = await inf_mai_bpm(result.query[int]("BPM查歌.bpm"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("BPM查歌.page"):
                    page = result.query[int]("BPM查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 定数查歌
    if result.find("定数查歌"):
        message_occurred()
        difficulty = result.query[str]("定数查歌.difficulty")
        m = await inf_mai_decimal(difficulty, result.query[float]("定数查歌.decimal"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("定数查歌.page"):
                    page = result.query[int]("定数查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 等级查歌
    if result.find("等级查歌"):
        message_occurred()
        difficulty = result.query[str]("等级查歌.difficulty")
        m = await inf_mai_level(difficulty, result.query[str]("等级查歌.level"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("等级查歌.page"):
                    page = result.query[int]("等级查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 物量查歌
    if result.find("物量查歌"):
        message_occurred()
        m = await inf_mai_total(result.query[int]("物量查歌.total_notes"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("物量查歌.page"):
                    page = result.query[int]("物量查歌.page.page")
                await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 查看别名
    if result.find("查看别名"):
        message_occurred()
        m = await inf_mai_seek_aliases(result.query[int]("查看别名.music_id"))
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 随歌
    if result.find("随歌"):
        message_occurred()
        m = await inf_mai_roll()
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()) + MessageSegment.text(m.build()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 定数随歌
    if result.find("定数随歌"):
        message_occurred()
        difficulty = result.query[str]("定数随歌.difficulty")
        if not difficulty:
            difficulty = ""
        m = await inf_mai_roll_by_decimal(difficulty, result.query[float]("定数随歌.decimal"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()) + MessageSegment.text(m.build()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 等级随歌
    if result.find("等级随歌"):
        message_occurred()
        difficulty = result.query[str]("等级随歌.difficulty")
        if not difficulty:
            difficulty = ""
        m = await inf_mai_roll_by_level(difficulty, result.query[str]("等级随歌.level"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()) + MessageSegment.text(m.build()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 定数表
    if result.find("定数表"):
        message_occurred()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))

    # 命令mai 牌子条件
    if result.find("牌子条件"):
        message_occurred()
        m = await inf_mai_plate_requirement()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))

    # 命令mai ra计算
    if result.find("ra计算"):
        message_occurred()
        m = await inf_mai_ra_calculating(result.query[float]("ra计算.decimal"), result.query[float]("ra计算.acc"))
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 分数线
    if result.find("分数线"):
        message_occurred()
        difficulty = result.query[str]("分数线.difficulty")
        if difficulty == "":
            difficulty = "紫"
        m = await inf_mai_score_line_v1(difficulty, result.query[int]("分数线.music_id"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 段位认定
    if result.find("段位认定"):
        message_occurred()
        m = await inf_mai_course()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))

    # 命令mai 真段位认定
    if result.find("真段位认定"):
        message_occurred()
        m = await inf_mai_shincourse()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))

    # 命令mai 随机段位认定
    if result.find("随机段位认定"):
        message_occurred()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))

    # 命令mai 友人对战
    if result.find("友人对战"):
        message_occurred()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))

    # 命令mai 查找机厅
    if result.find("查找机厅"):
        message_occurred()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))

    # 命令mai b50
    if result.find("b50"):
        message_occurred()
        username = result.query[str]("b50.username")
        friend_code = result.query[str]("b50.friend_code")
        is_lxns = True if result.find("b50.lxns") else False
        if username:
            m = await inf_mai_b50_v1(username, "")
        else:
            m = await inf_mai_b50_v1("", str(event.user_id))
        if is_lxns:
            m = await inf_mai_b50_v1("", "", is_lxns, friend_code)
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai ap50
    if result.find("ap50"):
        message_occurred()
        username = result.query[str]("ap50.username")
        friend_code = result.query[str]("ap50.friend_code")
        is_lxns = True if result.find("ap50.lxns") else False
        if username:
            m = await inf_mai_ap50_v1(username, "")
        else:
            m = await inf_mai_ap50_v1("", str(event.user_id))
        if is_lxns:
            m = await inf_mai_ap50_v1("", "", is_lxns, friend_code)
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

    # 命令mai 等级进度。
    if result.find("等级进度"):
        message_occurred()
        await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))

    # 命令mai 分数列表
    if result.find("分数列表"):
        message_occurred()
        page = result.query[int]("分数列表.page.page")
        m = await inf_mai_level_score_list_v1(str(event.user_id), result.query[str]("分数列表.level"), page)
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id)+ MessageSegment.text(m.build()))

    # 命令mai score
    if result.find("score"):
        message_occurred()
        m = await inf_mai_score_v1(str(event.user_id), result.query[str]("score.music_id"))
        if m.status:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await mai_command.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))


@what_song_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    keyword = result.header["keyword"]
    m = await inf_mai_what_song(keyword)
    if m.status:
        if m.is_paged:
            page = 1
            if result.find("page"):
                page = result.query[int]("page.page")
            await what_song_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build(page)))
        await what_song_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
    else:
        await what_song_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

@version_song_list_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    version = result.header["version"]
    m = await inf_mai_plate_song_list_v1(version)
    if m.status:
        await version_song_list_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
    else:
        await version_song_list_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

@level_and_plate_completion_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    keyword = result.header["keyword"]
    if check_level(keyword):
        await level_and_plate_completion_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))
    else:
        m = await inf_mai_plate_completion_v1(event.user_id, keyword)
        if m.status:
            await version_song_list_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.image(m.get_image()))
        else:
            await version_song_list_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))

@level_process_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    keyword = result.header["keyword"]
    if check_level(keyword):
        await level_process_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~"))
    m = await inf_mai_plate_process_v1(str(event.user_id), keyword)
    await level_process_cmd.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(m.build()))