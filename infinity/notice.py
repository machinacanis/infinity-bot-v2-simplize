from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot

import infinity
from infinity.model.uni_message import InfinityUniMessage


# 调用后将通知消息发送到管理员和管理群组
async def notice(bot: Bot, message: str | InfinityUniMessage):
    if isinstance(message, str):
        msg = message
    else:
        msg = message.build()
    # 对管理员转发消息
    for superuser in infinity.superusers:
        await bot.send_private_msg(user_id=superuser, message=msg)
    # 对管理群组转发消息
    for supergroup in infinity.supergroups:
        await bot.send_group_msg(group_id=supergroup, message=msg)

    logger.info("管理通知消息已发送")
