import random

from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot_plugin_alconna import Alconna, Args, Match, on_alconna

from infinity import message_occurred
from infinity.rules import is_allowed

choose = on_alconna(Alconna("做选择", Args["payload?", str]), use_cmd_start=True, use_cmd_sep=True, aliases={"choose"}, rule=is_allowed)


@choose.handle()
async def _(event: GroupMessageEvent | PrivateMessageEvent, payload: Match[str]):
        if "还是" in payload.result:
            choices = payload.result.split("还是")
            choices = [choice for choice in choices if choice]
            if len(choices) == 0:
                message_occurred()
                await choose.finish(MessageSegment.reply(event.message_id) + f"建议您爬捏！")
            if len(choices) < 2:
                message_occurred()
                await choose.finish(MessageSegment.reply(event.message_id) + "请至少提供 2 个选项，并以“还是”隔开")
            # 生成一个随机数
            r = random.random()
            
            # 70% 概率执行代码块 A
            if r < 0.7:
                message_occurred()
                await choose.finish(MessageSegment.reply(event.message_id) + f"建议您选择{random.choice(choices)}捏！")
            # 30% 概率执行代码块 B
            else:
                msg = ["建议您全都要捏！", "建议您全都不要捏！", "建议您随便捏！"]
                message_occurred()
                await choose.finish(MessageSegment.reply(event.message_id) + random.choice(msg))
