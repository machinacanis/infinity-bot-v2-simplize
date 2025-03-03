from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import (
    PrivateMessageEvent,
    GroupMessageEvent,
    MessageSegment,
    Bot,
)
from nonebot.rule import to_me
from nonebot_plugin_alconna import on_alconna

from infinity import message_occurred
from infinity.infinity_api_v1 import inf_hello_world, inf_ping, inf_help
from infinity.rules import is_allowed

help_command = on_alconna(
    Alconna("help"), priority=10, use_cmd_start=True, use_cmd_sep=True, rule=is_allowed
)


@help_command.handle()
async def _(bot: Bot, event: PrivateMessageEvent | GroupMessageEvent):
    message_occurred()
    msg = await inf_help()
    await help_command.finish(
        MessageSegment.reply(event.message_id) + MessageSegment.image(msg.get_image())
    )
