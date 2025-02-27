import asyncio

from nonebot import on_notice, get_driver, logger
from nonebot.adapters.onebot.v11 import GroupBanNoticeEvent, GroupDecreaseNoticeEvent, GroupMessageEvent, \
    PrivateMessageEvent, Bot
from arclet.alconna import Alconna, Args
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna, Match

from infinity.mongodb_connect import connection as gm
from infinity.rules import is_allowed, is_superuser

enable_group_command = on_alconna(
    Alconna(
        "开启群",
        Args["group_id", int]
    ), use_cmd_sep=True, use_cmd_start=True, rule=is_superuser
)
disable_group_command = on_alconna(
    Alconna(
        "关闭群",
        Args["group_id", int]
    ), use_cmd_sep=True, use_cmd_start=True, rule=is_superuser
)
ban_user_command = on_alconna(
    Alconna(
        "拉黑",
        Args["user_id", int]
    ), use_cmd_sep=True, use_cmd_start=True, rule=is_superuser
)
unban_user_command = on_alconna(
    Alconna(
        "解黑",
        Args["user_id", int]
    ), use_cmd_sep=True, use_cmd_start=True, rule=is_superuser
)
update_cmd = on_alconna(
    Alconna(
        "update",
    ), use_cmd_sep=True, use_cmd_start=True, rule=is_superuser
)

group_mute_event = on_notice(is_type(GroupBanNoticeEvent))
group_decrease_event = on_notice(is_type(GroupDecreaseNoticeEvent))


@enable_group_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, group_id: Match[int]):
    pass

@disable_group_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, group_id: Match[int]):
    pass

@ban_user_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, user_id: Match[int]):
    pass

@unban_user_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, user_id: Match[int]):
    pass

@update_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, type: Match[str]):
    """用于拉起一次全量数据更新的方法"""
    logger.info("开始拉取全量更新数据")
    await update_cmd.send("开始进行全量更新。", is_reply=True)
    await asyncio.gather(
        gm.get_maimai_song_data_from_lx(),
        gm.get_chunithm_songs_data_from_lx(),
        gm.get_maimai_aliases_from_fanyu(),
        gm.get_chunithm_aliases_from_lx(),
        gm.get_maimai_arcade_data_from_wahlap(),
        gm.get_chunithm_arcade_data_from_wahlap()
    )
    logger.info("全量更新数据拉取完成")
    await asyncio.gather(
        gm.update_maimai_song_data(),
        gm.update_chunithm_song_data(),
        gm.update_maimai_alias_data(),
        gm.update_chunithm_alias_data(),
        gm.update_maimai_arcade_data(),
        gm.update_chunithm_arcade_data()
    )
    await update_cmd.finish("全量更新数据拉取完成。", is_reply=True)