from nonebot import logger

from infinity.infinity_api_v1 import inf_mai_b50_v1
from infinity.maimai_lib_v1.mai_plate_completion import draw_user_music_info
from infinity.mongodb_connect import connection as gm
from infinity.userdata_client_v2 import DivingFishClient


async def db_refresh():
    gm.create_connection()

    async def update():
        """用于拉起一次全量数据更新的方法"""
        logger.info("开始拉取全量更新数据")
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

    await update()


async def main():
    img = await inf_mai_b50_v1("2913844577")
    img.show()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
