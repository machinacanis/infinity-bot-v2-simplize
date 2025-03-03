from arclet.alconna import Arparma, Option
from nonebot import on_notice, get_driver
from nonebot.adapters.onebot.v11 import (
    GroupBanNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    Bot,
    MessageSegment,
)
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna, Match, Alconna, Args, Subcommand

from infinity import message_occurred
from infinity.infinity_api_v1 import (
    inf_chu_help,
    inf_chu_id,
    inf_chu_song,
    inf_chu_chart,
    inf_chu_chage,
    inf_chu_search,
    inf_chu_artist,
    inf_chu_bpm,
    inf_chu_decimal,
    inf_chu_level,
    inf_chu_total,
    inf_chu_seek_aliases,
    inf_chu_roll,
    inf_chu_roll_by_decimal,
    inf_chu_roll_by_level,
    inf_chu_ra_calculating,
)
from infinity.rules import is_allowed

# noinspection PyTypeChecker
chu_command = on_alconna(
    Alconna(
        "chu",
        Subcommand("help"),
        Subcommand("id", Args["music_id", int]),
        Subcommand("song", Args["music_id", int]),
        Subcommand("chart", Args["music_id", int]["difficulty", str]),
        Subcommand(
            "查歌",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand(
            "search",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand(
            "曲师查歌",
            Args["keyword", str],
            Option("-p|--page", Args["page", int], default=1),
            alias=["艺术家查歌", "artist"],
        ),
        Subcommand(
            "BPM查歌",
            Args["bpm", int],
            Option("-p|--page", Args["page", int], default=1),
            alias=["bpm查歌", "bpm"],
        ),
        Subcommand(
            "定数查歌",
            Args["decimal", float]["difficulty?", str],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand(
            "等级查歌",
            Args["level", str]["difficulty?", str],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand(
            "物量查歌",
            Args["total_notes", int],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand(
            "查看别名",
            Args["music_id", int],
            Option("-p|--page", Args["page", int], default=1),
        ),
        Subcommand("随歌", alias=["random"]),
        Subcommand("定数随歌", Args["decimal", float]["difficulty?", str]),
        Subcommand("等级随歌", Args["level", str]["difficulty?", str]),
        Subcommand("定数表", Args["level", str]),
        Subcommand("ra计算", Args["decimal", float]["acc", float]),
    ),
    use_cmd_start=True,
    use_cmd_sep=True,
    rule=is_allowed,
)


@chu_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    # 命令chu help
    if result.find("help"):
        message_occurred()
        m = await inf_chu_help()
        await chu_command.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
        )

    # 命令chu id
    elif result.find("id"):
        message_occurred()
        m = await inf_chu_id(result.query[int]("id.music_id"))
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu song
    if result.find("song"):
        message_occurred()
        m = await inf_chu_song(result.query[int]("song.music_id"))
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
                + MessageSegment.text(m.build())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu chart
    if result.find("chart"):
        message_occurred()
        m = await inf_chu_chart(
            result.query[str]("chart.difficulty"), result.query[int]("chart.music_id")
        )
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
                + MessageSegment.text(m.build())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 查歌
    if result.find("查歌"):
        message_occurred()
        m = await inf_chu_chage(result.query[str]("查歌.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("查歌.page"):
                    page = result.query[int]("查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu search
    if result.find("search"):
        message_occurred()
        m = await inf_chu_search(result.query[str]("search.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("search.page"):
                    page = result.query[int]("search.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 曲师查歌
    if result.find("曲师查歌"):
        message_occurred()
        m = await inf_chu_artist(result.query[str]("曲师查歌.keyword"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("曲师查歌.page"):
                    page = result.query[int]("曲师查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu BPM查歌
    if result.find("BPM查歌"):
        message_occurred()
        m = await inf_chu_bpm(result.query[int]("BPM查歌.bpm"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("BPM查歌.page"):
                    page = result.query[int]("BPM查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 定数查歌
    if result.find("定数查歌"):
        message_occurred()
        difficulty = result.query[str]("定数查歌.difficulty")
        m = await inf_chu_decimal(difficulty, result.query[float]("定数查歌.decimal"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("定数查歌.page"):
                    page = result.query[int]("定数查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 等级查歌
    if result.find("等级查歌"):
        message_occurred()
        difficulty = result.query[str]("等级查歌.difficulty")
        m = await inf_chu_level(difficulty, result.query[str]("等级查歌.level"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("等级查歌.page"):
                    page = result.query[int]("等级查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 物量查歌
    if result.find("物量查歌"):
        message_occurred()
        m = await inf_chu_total(result.query[int]("物量查歌.total_notes"))
        if m.status:
            if m.is_paged:
                page = 1
                if result.find("物量查歌.page"):
                    page = result.query[int]("物量查歌.page.page")
                await chu_command.finish(
                    MessageSegment.reply(event.message_id)
                    + MessageSegment.text(m.build(page))
                )
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 查看别名
    if result.find("查看别名"):
        message_occurred()
        m = await inf_chu_seek_aliases(result.query[int]("查看别名.music_id"))
        await chu_command.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
        )

    # 命令chu 随歌
    if result.find("随歌"):
        message_occurred()
        m = await inf_chu_roll()
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
                + MessageSegment.text(m.build())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 定数随歌
    if result.find("定数随歌"):
        message_occurred()
        difficulty = result.query[str]("定数随歌.difficulty")
        if not difficulty:
            difficulty = ""
        m = await inf_chu_roll_by_decimal(
            difficulty, result.query[float]("定数随歌.decimal")
        )
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
                + MessageSegment.text(m.build())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 等级随歌
    if result.find("等级随歌"):
        message_occurred()
        difficulty = result.query[str]("等级随歌.difficulty")
        if not difficulty:
            difficulty = ""
        m = await inf_chu_roll_by_level(difficulty, result.query[str]("等级随歌.level"))
        if m.status:
            await chu_command.finish(
                MessageSegment.reply(event.message_id)
                + MessageSegment.image(m.get_image())
                + MessageSegment.text(m.build())
            )
        else:
            await chu_command.finish(
                MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
            )

    # 命令chu 定数表
    if result.find("定数表"):
        message_occurred()
        await chu_command.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.text("🚧施工中~")
        )

    # 命令chu ra计算
    if result.find("ra计算"):
        message_occurred()
        m = await inf_chu_ra_calculating(
            result.query[float]("ra计算.decimal"), result.query[float]("ra计算.acc")
        )
        await chu_command.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.text(m.build())
        )
