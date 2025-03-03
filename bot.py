import os
import sys

import dotenv
import nonebot
from nonebot import logger
from nonebot.adapters.onebot import V11Adapter  # 避免重复命名

from infinity import (
    set_start_time,
    init_hourly_message_processed,
    connection,
    mongo_url,
    mongo_user,
    mongo_password,
)

# 初始化
dotenv.load_dotenv()
set_start_time()
init_hourly_message_processed()

# 加载数据库连接
connection.create_connection(mongo_url, mongo_user, mongo_password)

logger.remove()
logger.level("DEBUG", color="<blue>", icon="[__DEBUG]")
logger.level("INFO", color="<white>", icon="[___INFO]")
logger.level("SUCCESS", color="<green>", icon="[SUCCESS]")
logger.level("WARNING", color="<yellow>", icon="[WARNING]")
logger.level("ERROR", color="<red>", icon="[__ERROR]")
default_format: str = (
    "<cyan>{time:MM/DD HH:mm:ss}</cyan> <lvl>{level.icon}</lvl> {message}"
)
infinity_logger_id = logger.add(
    sys.stdout,
    level=os.getenv("LOG_LEVEL", "INFO"),
    diagnose=False,
    format=default_format,
)

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)

# 在这里加载插件
nonebot.load_plugins("./plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()
    # 关闭数据库连接
    connection.close_connection()
