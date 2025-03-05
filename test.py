import dotenv
from nonebot import logger

from infinity import connection, mongo_url, mongo_user, mongo_password
from infinity.chunithm_previewer_v1 import get_chunithm_preview_v1


async def main():
    # 初始化
    dotenv.load_dotenv()
    # 加载数据库连接
    connection.create_connection(mongo_url, mongo_user, mongo_password)

    res = await get_chunithm_preview_v1(2399)
    print(res)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
