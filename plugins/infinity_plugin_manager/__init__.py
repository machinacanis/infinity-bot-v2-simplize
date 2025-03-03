import asyncio

from nonebot import on_notice, get_driver, logger
from nonebot.adapters.onebot.v11 import (
    GroupBanNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    Bot,
)
from arclet.alconna import Alconna, Args, Arparma
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna, Match

from infinity import (
    add_whitelist_qq_group,
    remove_whitelist_qq_group,
    add_banned_qq_user,
    get_instance_qid,
    message_occurred,
    update_whitelist_and_banned_list,
    send_start_message,
    send_shutdown_message,
)
from infinity.mongodb_connect import connection as gm
from infinity.notice import notice
from infinity.rules import is_allowed, is_superuser

driver = get_driver()

enable_group_command = on_alconna(
    Alconna("开启群", Args["group_id", int]),
    use_cmd_sep=True,
    use_cmd_start=True,
    rule=is_superuser,
)
disable_group_command = on_alconna(
    Alconna("关闭群", Args["group_id", int]),
    use_cmd_sep=True,
    use_cmd_start=True,
    rule=is_superuser,
)
ban_user_command = on_alconna(
    Alconna("拉黑", Args["user_id", int]),
    use_cmd_sep=True,
    use_cmd_start=True,
    rule=is_superuser,
)
unban_user_command = on_alconna(
    Alconna("解黑", Args["user_id", int]),
    use_cmd_sep=True,
    use_cmd_start=True,
    rule=is_superuser,
)
update_cmd = on_alconna(
    Alconna(
        "update",
    ),
    use_cmd_sep=True,
    use_cmd_start=True,
    rule=is_superuser,
)

group_mute_event = on_notice(is_type(GroupBanNoticeEvent))
group_decrease_event = on_notice(is_type(GroupDecreaseNoticeEvent))


@driver.on_bot_connect
async def _(bot: Bot):
    if send_start_message:
        msg = "Infinity Bot V2已连接！"
        await notice(bot, msg)


@driver.on_bot_disconnect
async def _(bot: Bot):
    if send_shutdown_message:
        msg = "Infinity Bot V2已断开连接！"
        await notice(bot, msg)


@driver.on_startup
async def _():
    await update_whitelist_and_banned_list()


@enable_group_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    targer_id = result.query[int]("group_id")
    await add_whitelist_qq_group(targer_id)
    await notice(bot, f"群 {targer_id} 已被启用！")


@disable_group_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    targer_id = result.query[int]("group_id")
    await remove_whitelist_qq_group(targer_id)
    await notice(bot, f"群 {targer_id} 已被禁用！")


@ban_user_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    target_id = result.query[int]("user_id")
    await add_banned_qq_user(target_id)
    await notice(bot, f"用户 {target_id} 已被拉黑！")


@unban_user_command.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, result: Arparma):
    message_occurred()
    target_id = result.query[int]("user_id")
    await add_banned_qq_user(target_id)
    await notice(bot, f"用户 {target_id} 已被解黑！")


@update_cmd.handle()
async def _(bot: Bot):
    """用于拉起一次全量数据更新的方法"""
    message_occurred()
    logger.info("开始拉取全量更新数据")
    await notice(bot, "开始拉取全量更新数据")
    await asyncio.gather(
        gm.get_maimai_song_data_from_lx(),
        gm.get_chunithm_songs_data_from_lx(),
        gm.get_maimai_aliases_from_fanyu(),
        gm.get_chunithm_aliases_from_lx(),
        gm.get_maimai_arcade_data_from_wahlap(),
        gm.get_chunithm_arcade_data_from_wahlap(),
    )
    logger.info("全量更新数据拉取完成")
    await asyncio.gather(
        gm.update_maimai_song_data(),
        gm.update_chunithm_song_data(),
        gm.update_maimai_alias_data(),
        gm.update_chunithm_alias_data(),
        gm.update_maimai_arcade_data(),
        gm.update_chunithm_arcade_data(),
    )
    await notice(bot, "全量更新数据拉取完成")


@group_mute_event.handle()
async def _(bot: Bot, event: GroupBanNoticeEvent):
    message_occurred()
    # Bot被禁言了
    group_name: dict = await bot.get_group_info(group_id=event.group_id)
    msg = f"在群组 {event.group_id} 被管理员 {event.user_id} 禁言了！\n群聊名称：{group_name['group_name']}"
    # 向超级用户和集散群通告
    await notice(bot, msg)


@group_decrease_event.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    message_occurred()
    res = await get_instance_qid(bot)
    if event.user_id == res:
        # Bot被踢出了
        msg = f"在群组 {event.group_id} 被踢出了！"
        # 向超级用户和集散群通告
        await notice(bot, msg)
