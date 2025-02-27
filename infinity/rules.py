from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

import infinity.whitelist


async def is_allowed(event: PrivateMessageEvent | GroupMessageEvent) -> bool:
    # 用于检测触发事件的用户是否符合预设条件的规则
    if isinstance(event, GroupMessageEvent):
        # 是群消息
        # 判断是否在白名单中
        if event.group_id in infinity.whitelist.whitelisted_qq_groups:
            pass
        else:
            return False
    # 检测是否在用户黑名单中
    if event.user_id in infinity.whitelist.banned_qq_users:
        return False
    return True

async def is_superuser(event: PrivateMessageEvent | GroupMessageEvent) -> bool:
    # 用于检测触发事件的用户是否具有超级用户权限
    if event.user_id in infinity.superusers:
        return True
    else:
        return False