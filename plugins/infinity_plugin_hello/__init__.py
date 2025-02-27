from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, MessageSegment
from nonebot.rule import to_me
from nonebot_plugin_alconna import on_alconna

from infinity import message_occurred
from infinity.infinity_api_v1 import inf_hello_world
from infinity.rules import is_allowed

hello_world_command = on_alconna(
    Alconna(
        "helloworld"
    ), priority=10, use_cmd_start=True, use_cmd_sep=True,
    rule=is_allowed
)

@hello_world_command.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent):
    message_occurred()
    msg = await inf_hello_world()
    await hello_world_command.finish(MessageSegment.reply(event.message_id) + msg.build())