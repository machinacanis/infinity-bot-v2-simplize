from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import (
    PrivateMessageEvent,
    GroupMessageEvent,
    MessageSegment,
    Bot,
)
from nonebot.permission import Permission, SUPERUSER
from nonebot.rule import to_me
from nonebot_plugin_alconna import on_alconna

from infinity import message_occurred
from infinity.infinity_api_v1 import inf_hello_world, inf_ping
from infinity.rules import is_allowed

ping_command = on_alconna(
    Alconna("ping"), priority=10, use_cmd_start=True, use_cmd_sep=True, rule=is_allowed
)


@ping_command.handle()
async def _(bot: Bot, event: PrivateMessageEvent | GroupMessageEvent):
    message_occurred()
    is_admin = await SUPERUSER(bot, event)
    msg = await inf_ping(bot, is_admin)
    await ping_command.finish(MessageSegment.reply(event.message_id) + msg.build())
