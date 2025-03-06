import base64

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot_plugin_alconna import on_alconna

from .data import fortune_manager
from .utils import drawing

today = on_alconna(Alconna("today"), use_cmd_sep=True, use_cmd_start=True)


@today.handle()
async def _(event: GroupMessageEvent | PrivateMessageEvent, matcher: Matcher):
    uid: str = str(event.get_user_id())
    _, image_file_a = fortune_manager.divine(uid)
    # image_file_a = drawing(uid)
    with open(image_file_a, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        image_file_base64 = f"base64://{encoded_image}"

        msg = MessageSegment.image(image_file_base64)

    await today.finish(msg, reply_message=True)

