from typing import Mapping, Any

import httpx
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from nonebot import logger

import infinity
from .cache_manager import CacheManager
from .model import ChuniSongData, ArcadeInfo
from .model.chunithm_song import create_chuni_song_data, ChuniDifficulty
from .model.maimai_song import create_maimai_song_data, MaimaiSongData, MaiDifficulty
from .utils import is_dx, deduplicate


class MongoDBConnect:
    client: AsyncIOMotorClient  # MongoDB的异步客户端对象

    # 数据库集合对象
    info_collection: AsyncIOMotorCollection[
        Mapping[str, Any]
    ]  # Infinity Bot的部分操作信息
    maimai_song_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    maimai_alias_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    chunithm_song_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    chunithm_alias_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    maimai_arcade_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    chunithm_arcade_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    group_whitelist_collection: AsyncIOMotorCollection[Mapping[str, Any]]
    user_blacklist_collection: AsyncIOMotorCollection[Mapping[str, Any]]

    # 数据拉取缓存，这部分变量应该在处理之后被清空
    maimai_song_data: list[MaimaiSongData]
    maimai_alias_data: list[dict]
    chunithm_song_data: list[ChuniSongData]
    chunithm_alias_data: list[dict]
    maimai_arcade_data: list[dict]
    chunithm_arcade_data: list[dict]

    # 缓存管理器实例
    cache = CacheManager("gamedata", 512)

    def create_connection(
        self,
        url="mongodb://localhost:27017",
        username="",
        password="",
        max_pool_size=100,
        min_pool_size=10,
    ):
        """用于与MongoDB建立连接的方法"""
        if username and password:
            self.client = AsyncIOMotorClient(
                url,
                username=username,
                password=password,
                maxPoolSize=max_pool_size,
                minPoolSize=min_pool_size,
            )
        else:
            self.client = AsyncIOMotorClient(
                url, maxPoolSize=max_pool_size, minPoolSize=min_pool_size
            )

        self.maimai_song_collection = self.client["infinity"]["maimai_song"]
        self.maimai_alias_collection = self.client["infinity"]["maimai_alias"]
        self.chunithm_song_collection = self.client["infinity"]["chunithm_song"]
        self.chunithm_alias_collection = self.client["infinity"]["chunithm_alias"]
        self.maimai_arcade_collection = self.client["infinity"]["maimai_arcade_list"]
        self.chunithm_arcade_collection = self.client["infinity"][
            "chunithm_arcade_list"
        ]
        self.group_whitelist_collection = self.client["infinity"]["group_whitelist"]
        self.user_blacklist_collection = self.client["infinity"]["user_blacklist"]

    def close_connection(self):
        """关闭数据库连接的方法"""
        self.client.close()

    async def get_maimai_song_data_from_lx(self):
        """从maimai.lxns.net拉取maimai的歌曲数据"""
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    infinity.lx_api + "maimai/song/list?notes=true",
                    headers={"Authorization": infinity.lx_token},
                )
                if resp.status_code == 200:
                    self.maimai_song_data = create_maimai_song_data(
                        resp.json()["songs"]
                    )
                else:
                    logger.warning(
                        f"与落雪API通信获取舞萌歌曲数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
            except Exception as e:
                logger.error(f"尝试从落雪API获取舞萌歌曲数据时发生错误：{e}")

    async def get_chunithm_songs_data_from_lx(self):
        """从maimai.lxns.net拉取maimai的歌曲数据"""
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    infinity.lx_api + "chunithm/song/list?notes=true",
                    headers={"Authorization": infinity.lx_token},
                )
                if resp.status_code == 200:
                    self.chunithm_song_data = create_chuni_song_data(
                        resp.json()["songs"]
                    )
                else:
                    logger.warning(
                        f"与落雪API通信获取中二歌曲数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
            except Exception as e:
                logger.error(f"尝试从落雪API获取中二节奏歌曲数据时发生错误：{e}")

    async def get_maimai_aliases_from_fanyu(self):
        """获取舞萌别名"""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(infinity.fanyu_api + "maimai/alias.json")
                if resp.status_code == 200:
                    alias: dict = resp.json()
                    # 将别名字典解压成键值对列表
                    alias_list = [
                        {"musicId": key, "aliases": value}
                        for key, value in alias.items()
                    ]
                    self.maimai_alias_data = alias_list
                else:
                    logger.warning(
                        f"与fanyu API通信获取舞萌别名数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
        except Exception as e:
            logger.error(f"尝试从fanyu API获取舞萌别名数据时发生错误：{e}")
            return {}

    async def get_maimai_aliases_from_lx(self):
        """获取舞萌别名"""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    infinity.lx_api + "maimai/alias/list",
                    headers={"Authorization": infinity.lx_token},
                )
                # 判断请求是否成功
                if resp.status_code == 200:
                    data = resp.json()

                    # 解析数据格式
                    alias_list = [
                        {"musicId": item["song_id"], "aliases": item["aliases"]}
                        for item in data["aliases"]
                    ]

                    # 存储解析后的数据
                    self.maimai_alias_data = alias_list
                else:
                    logger.warning(
                        f"与落雪API通信获取舞萌别名数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
        except Exception as e:
            logger.error(f"尝试从落雪API获取舞萌别名数据时发生错误：{e}")
            return {}

    async def get_chunithm_aliases_from_lx(self):
        """获取中二别名"""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    infinity.lx_api + "chunithm/alias/list",
                    headers={"Authorization": infinity.lx_token},
                )
                # 判断请求是否成功
                if resp.status_code == 200:
                    data = resp.json()

                    # 解析数据格式
                    alias_list = [
                        {"musicId": item["song_id"], "aliases": item["aliases"]}
                        for item in data["aliases"]
                    ]

                    # 存储解析后的数据
                    self.chunithm_alias_data = alias_list
                else:
                    logger.warning(
                        f"与落雪API通信获取中二别名数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
        except Exception as e:
            logger.error(f"尝试从落雪API获取中二别名数据时发生错误：{e}")
            return {}

    async def get_maimai_arcade_data_from_wahlap(self):
        """获取舞萌机台数据"""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    infinity.wahlap_arcade_api + "maidx/rest/location"
                )
                if resp.status_code == 200:
                    self.maimai_arcade_data = resp.json()
                else:
                    logger.warning(
                        f"与华立API通信获取舞萌机台数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
        except Exception as e:
            logger.error(f"尝试从华立API获取舞萌机台数据时发生错误：{e}")

    async def get_chunithm_arcade_data_from_wahlap(self):
        """获取中二机台数据"""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    infinity.wahlap_arcade_api + "chunithm/rest/location"
                )
                if resp.status_code == 200:
                    self.chunithm_arcade_data = resp.json()
                else:
                    logger.warning(
                        f"与华立API通信获取中二机台数据时发出现问题，状态码：{resp.status_code}，已跳过这次数据拉取"
                    )
        except Exception as e:
            logger.error(f"尝试从华立API获取中二机台数据时发生错误：{e}")

    async def update_maimai_song_data(self):
        """更新舞萌歌曲数据"""
        try:
            if self.maimai_song_data is None:
                logger.warning(
                    "未检测到舞萌歌曲数据，更新前需要先从落雪API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新舞萌歌曲数据，此次更新共有{len(self.maimai_song_data)}首歌曲"
            )
            # 清除原有数据
            await self.maimai_song_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            songs_dict = [song.to_dict() for song in self.maimai_song_data]
            await self.maimai_song_collection.insert_many(songs_dict)
        except Exception as e:
            logger.error(f"更新舞萌歌曲数据时发生错误：{e}")

    async def update_chunithm_song_data(self):
        """更新中二歌曲数据"""
        try:
            if self.chunithm_song_data is None:
                logger.warning(
                    "未检测到中二歌曲数据，更新前需要先从落雪API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新中二歌曲数据，此次更新共有{len(self.chunithm_song_data)}首歌曲"
            )
            # 清除原有数据
            await self.chunithm_song_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            songs_dict = [song.to_dict() for song in self.chunithm_song_data]
            await self.chunithm_song_collection.insert_many(songs_dict)
        except Exception as e:
            logger.error(f"更新中二歌曲数据时发生错误：{e}")

    async def update_maimai_alias_data(self):
        """更新舞萌别名数据"""
        try:
            if self.maimai_alias_data is None:
                logger.warning(
                    "未检测到舞萌别名数据，更新前需要先从fanyu API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新舞萌别名数据，此次更新共有{len(self.maimai_alias_data)}首歌曲"
            )
            # 清除原有数据
            await self.maimai_alias_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            await self.maimai_alias_collection.insert_many(self.maimai_alias_data)
        except Exception as e:
            logger.error(f"更新舞萌别名数据时发生错误：{e}")

    async def update_chunithm_alias_data(self):
        """更新中二别名数据"""
        try:
            if self.chunithm_alias_data is None:
                logger.warning(
                    "未检测到中二别名数据，更新前需要先从落雪API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新中二别名数据，此次更新共有{len(self.chunithm_alias_data)}首歌曲"
            )
            # 清除原有数据
            await self.chunithm_alias_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            await self.chunithm_alias_collection.insert_many(self.chunithm_alias_data)
        except Exception as e:
            logger.error(f"更新中二别名数据时发生错误：{e}")

    async def update_maimai_arcade_data(self):
        """更新舞萌机台数据"""
        try:
            if self.maimai_arcade_data is None:
                logger.warning(
                    "未检测到舞萌机台数据，更新前需要先从华立API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新舞萌机台数据，此次更新共有{len(self.maimai_arcade_data)}个机台"
            )
            # 清除原有数据
            await self.maimai_arcade_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            await self.maimai_arcade_collection.insert_many(self.maimai_arcade_data)
        except Exception as e:
            logger.error(f"更新舞萌机台数据时发生错误：{e}")

    async def update_chunithm_arcade_data(self):
        """更新中二机台数据"""
        try:
            if self.chunithm_arcade_data is None:
                logger.warning(
                    "未检测到中二机台数据，更新前需要先从华立API拉取数据，已跳过更新"
                )
                return
            logger.info(
                f"开始向数据库中更新中二机台数据，此次更新共有{len(self.chunithm_arcade_data)}个机台"
            )
            # 清除原有数据
            await self.chunithm_arcade_collection.delete_many({})
            # 使用 insert_many 插入批量数据
            await self.chunithm_arcade_collection.insert_many(self.chunithm_arcade_data)
        except Exception as e:
            logger.error(f"更新中二机台数据时发生错误：{e}")

    async def query_maimai_song_by_id(self, mid: int):
        """根据歌曲id从数据库中查找歌曲数据"""
        # 先查缓存
        cache_key = f"maimai_song_id_{mid}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        # 缓存未命中，从数据库中查找
        res = await self.maimai_song_collection.find_one({"id": mid})
        if res:
            r = MaimaiSongData.from_dict(dict(res))
            self.cache.set(cache_key, r)  # 缓存结果
            return r
        return None

    async def query_maimai_chart_by_id_and_difficulty(
        self, mid: int, difficulty: MaiDifficulty
    ):
        """根据歌曲id和难度从数据库中查找谱面数据"""
        # 先查缓存
        cache_key = f"maimai_song_id_{mid}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            s = cached_result
        else:  # 缓存未命中，从数据库中查找
            res = await self.maimai_song_collection.find_one({"id": mid})
            s = MaimaiSongData.from_dict(dict(res))
        if s:
            self.cache.set(cache_key, s)  # 缓存结果
            if is_dx(mid):
                for chart in s.dx_charts:
                    if chart.difficulty == difficulty.int():
                        return chart
            else:
                for chart in s.sd_charts:
                    if chart.difficulty == difficulty.int():
                        return chart
        else:
            return None

    async def query_maimai_song_by_alias(self, alias: str) -> list[int]:
        """根据别名从数据库中检索歌曲，返回结果id列表"""
        res = await self.maimai_alias_collection.find(
            {"aliases": {"$regex": alias}}
        ).to_list()
        return [int(doc["musicId"]) for doc in res]

    async def query_maimai_song_by_keyword(self, keyword: str):
        """根据歌曲名称中的关键词从数据库中检索歌曲"""
        # 先查缓存
        cache_key = f"maimai_song_keyword_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        # 缓存未命中，从数据库中查找
        cur = self.maimai_song_collection.find({"title": {"$regex": keyword}})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_maimai_song_by_artist(self, keyword: str):
        """根据歌曲艺术家名称中的关键词从数据库中检索歌曲"""
        # 先查缓存
        cache_key = f"maimai_song_artist_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.maimai_song_collection.find({"artist": {"$regex": keyword}})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_maimai_song_by_bpm(self, bpm: int):
        """根据歌曲BPM从数据库中检索歌曲"""
        # 先查缓存
        cache_key = f"maimai_song_bpm_{bpm}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.maimai_song_collection.find({"bpm": bpm})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_maimai_song_by_decimal_and_difficulty(
        self, decimal: float, difficulty: MaiDifficulty
    ):
        """根据难度和定数从数据库中检索歌曲"""

        if difficulty.int() != -1:
            # 先查缓存
            cache_key = f"maimai_song_difficulty_{difficulty.str()}_decimal_{decimal}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {
                "$or": [
                    {
                        "sd_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                    {
                        "dx_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                    {
                        "utage_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                ]
            }
        else:
            # 查缓存
            cache_key = f"maimai_song_decimal_{decimal}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {
                "$or": [
                    {"sd_charts": {"$elemMatch": {"level_value": decimal}}},
                    {"dx_charts": {"$elemMatch": {"level_value": decimal}}},
                    {"utage_charts": {"$elemMatch": {"level_value": decimal}}},
                ]
            }
        cur = self.maimai_song_collection.find(query)
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        if difficulty:
            self.cache.set(
                f"maimai_song_difficulty_{difficulty.str()}_decimal_{decimal}",
                documents,
            )
        else:
            self.cache.set(f"maimai_song_decimal_{decimal}", documents)

        return documents

    async def query_maimai_song_by_level_and_difficulty(
        self, level: str, difficulty: MaiDifficulty
    ):
        """根据难度和等级从数据库中检索歌曲"""

        if difficulty.int() != -1:
            # 先查缓存
            cache_key = f"maimai_song_difficulty_{difficulty.str()}_level_{level}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {
                "$or": [
                    {
                        "sd_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                    {
                        "dx_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                    {
                        "utage_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                ]
            }
        else:
            # 查缓存
            cache_key = f"maimai_song_level_{level}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {
                "$or": [
                    {"sd_charts": {"$elemMatch": {"level": level}}},
                    {"dx_charts": {"$elemMatch": {"level": level}}},
                    {"utage_charts": {"$elemMatch": {"level": level}}},
                ]
            }
        cur = self.maimai_song_collection.find(query)
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        if difficulty:
            self.cache.set(
                f"maimai_song_difficulty_{difficulty.str()}_level_{level}", documents
            )
        else:
            self.cache.set(f"maimai_song_level_{level}", documents)
        return documents

    async def query_maimai_song_by_total_notes(self, total_notes: int):
        """根据谱面物量从数据库中检索歌曲"""
        # 先查缓存
        cache_key = f"maimai_song_total_{total_notes}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.maimai_song_collection.find(
            {
                "$or": [
                    {"sd_charts": {"$elemMatch": {"notes.total": total_notes}}},
                    {"dx_charts": {"$elemMatch": {"notes.total": total_notes}}},
                    {"utage_charts": {"$elemMatch": {"notes.total": total_notes}}},
                ]
            }
        )
        documents = []
        if cur:
            async for doc in cur:
                documents.append(MaimaiSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_maimai_aliases_by_id(self, mid: int) -> list[str] | None:
        """根据歌曲id获取别名"""
        res = await self.maimai_alias_collection.find_one({"musicId": str(mid)})
        if res:
            return res["aliases"]
        return None

    async def roll_maimai_song(self):
        """随机获取一首舞萌歌曲"""
        res = await self.maimai_song_collection.aggregate(
            [{"$sample": {"size": 1}}]
        ).to_list(length=None)
        if res:
            return MaimaiSongData.from_dict(res[0])
        return None

    async def roll_maimai_song_by_decimal_and_difficulty(
        self, decimal: float, difficulty: MaiDifficulty
    ):
        """随机获取一首指定定数的舞萌歌曲"""
        if difficulty.int() != -1:
            query = {
                "$or": [
                    {
                        "sd_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                    {
                        "dx_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                    {
                        "utage_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level_value": decimal,
                            }
                        }
                    },
                ]
            }
        else:
            query = {
                "$or": [
                    {"sd_charts": {"$elemMatch": {"level_value": decimal}}},
                    {"dx_charts": {"$elemMatch": {"level_value": decimal}}},
                    {"utage_charts": {"$elemMatch": {"level_value": decimal}}},
                ]
            }
        res = await self.maimai_song_collection.aggregate(
            [{"$match": query}, {"$sample": {"size": 1}}]
        ).to_list(length=None)
        if res:
            return MaimaiSongData.from_dict(res[0])
        return None

    async def roll_maimai_song_by_level_and_difficulty(
        self, level: str, difficulty: MaiDifficulty
    ):
        """随机获取一首指定等级的舞萌歌曲"""
        if difficulty.int() != -1:
            query = {
                "$or": [
                    {
                        "sd_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                    {
                        "dx_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                    {
                        "utage_charts": {
                            "$elemMatch": {
                                "difficulty": difficulty.int(),
                                "level": level,
                            }
                        }
                    },
                ]
            }
        else:
            query = {
                "$or": [
                    {"sd_charts": {"$elemMatch": {"level": level}}},
                    {"dx_charts": {"$elemMatch": {"level": level}}},
                    {"utage_charts": {"$elemMatch": {"level": level}}},
                ]
            }
        res = await self.maimai_song_collection.aggregate(
            [{"$match": query}, {"$sample": {"size": 1}}]
        ).to_list(length=None)
        if res:
            return MaimaiSongData.from_dict(res[0])
        return None

    async def query_chunithm_song_by_id(self, sid: int):
        """通过歌曲id查找中二歌曲信息，返回歌曲元数据"""
        cache_key = f"chunithm_song_id_{sid}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        res = await self.chunithm_song_collection.find_one({"id": sid})
        if res:
            r = ChuniSongData.from_dict(dict(res))
            self.cache.set(cache_key, r)
            return r
        return None

    async def query_chunithm_chart_by_id_and_difficulty(
        self, sid: int, difficulty: ChuniDifficulty
    ):
        """通过歌曲id和难度查找中二谱面信息，返回谱面元数据"""
        cache_key = f"chunithm_song_id_{sid}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            s = cached_result
        else:
            res = await self.chunithm_song_collection.find_one({"id": sid})
            s = ChuniSongData.from_dict(dict(res))
        if s:
            self.cache.set(cache_key, s)
            for chart in s.charts:
                if chart.difficulty == difficulty:
                    return chart
        else:
            return None

    async def query_chunithm_song_by_alias(self, alias: str) -> list[int]:
        """根据别名从数据库中检索歌曲，返回结果id列表"""
        res = await self.chunithm_alias_collection.find(
            {"aliases": {"$regex": alias}}
        ).to_list()
        return [doc["musicId"] for doc in res]

    async def query_chunithm_song_by_keyword(self, keyword: str):
        """根据歌曲名称中的关键词从数据库中检索中二歌曲"""
        cache_key = f"chunithm_song_keyword_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.chunithm_song_collection.find({"title": {"$regex": keyword}})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_chunithm_song_by_artist(self, keyword: str):
        """根据歌曲艺术家名称中的关键词从数据库中检索中二歌曲"""
        cache_key = f"chunithm_song_artist_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.chunithm_song_collection.find({"artist": {"$regex": keyword}})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_chunithm_song_by_bpm(self, bpm: int):
        """根据歌曲BPM从数据库中检索中二歌曲"""
        cache_key = f"chunithm_song_bpm_{bpm}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.chunithm_song_collection.find({"bpm": bpm})
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_chunithm_song_by_decimal_and_difficulty(
        self, decimal: float, difficulty: int | str | ChuniDifficulty = None
    ):
        """根据难度和定数从数据库中检索歌曲"""
        if difficulty.int() != -1:
            if not isinstance(difficulty, MaiDifficulty):
                difficulty = ChuniDifficulty(difficulty)
                # 先查缓存
                cache_key = (
                    f"chunithm_song_difficulty_{difficulty.str()}_decimal_{decimal}"
                )
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    return cached_result
            query = {
                "charts": {
                    "$elemMatch": {
                        "difficulty": difficulty.int(),
                        "level_value": decimal,
                    }
                }
            }
        else:
            # 查缓存
            cache_key = f"chunithm_song_decimal_{decimal}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {"charts": {"$elemMatch": {"level_value": decimal}}}
        cur = self.chunithm_song_collection.find(query)
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        if difficulty:
            self.cache.set(
                f"chunithm_song_difficulty_{difficulty.str()}_decimal_{decimal}",
                documents,
            )
        else:
            self.cache.set(f"chunithm_song_decimal_{decimal}", documents)

        return documents

    async def query_chunithm_song_by_level_and_difficulty(
        self, level: str, difficulty: int
    ):
        """根据难度和等级从数据库中检索中二歌曲"""
        if difficulty.int() != -1:
            if not isinstance(difficulty, MaiDifficulty):
                difficulty = ChuniDifficulty(difficulty)
                # 先查缓存
                cache_key = f"chunithm_song_difficulty_{difficulty.str()}_level_{level}"
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    return cached_result
            query = {
                "charts": {
                    "$elemMatch": {"difficulty": difficulty.int(), "level": level}
                }
            }
        else:
            # 查缓存
            cache_key = f"chunithm_song_level_{level}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            query = {"charts": {"$elemMatch": {"level": level}}}
        cur = self.chunithm_song_collection.find(query)
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        if difficulty:
            self.cache.set(
                f"chunithm_song_difficulty_{difficulty.str()}_level_{level}", documents
            )
        else:
            self.cache.set(f"chunithm_song_level_{level}", documents)

        return documents

    async def query_chunithm_song_by_total_notes(self, total_notes: int):
        """根据谱面物量从数据库中检索中二歌曲"""
        cache_key = f"chunithm_song_total_{total_notes}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        cur = self.chunithm_song_collection.find(
            {"charts": {"$elemMatch": {"notes.total": total_notes}}}
        )
        documents = []
        if cur:
            async for doc in cur:
                documents.append(ChuniSongData.from_dict(doc))
        else:
            return None
        self.cache.set(cache_key, documents)
        return documents

    async def query_chunithm_aliases_by_id(self, sid: int):
        """根据歌曲id获取别名"""
        res = await self.chunithm_alias_collection.find_one({"musicId": sid})
        if res:
            return res["aliases"]
        return None

    async def roll_chunithm_song(self):
        """随机获取一首中二歌曲"""
        res = await self.chunithm_song_collection.aggregate(
            [{"$sample": {"size": 1}}]
        ).to_list(length=None)
        if res:
            return ChuniSongData.from_dict(res[0])
        return None

    async def roll_chunithm_song_by_decimal_and_difficulty(
        self, decimal: float, difficulty: int
    ):
        """随机获取一首指定定数的中二歌曲"""
        if difficulty.int() != -1:
            res = await self.chunithm_song_collection.aggregate(
                [
                    {
                        "$match": {
                            "charts": {
                                "$elemMatch": {
                                    "difficulty": difficulty,
                                    "level_value": decimal,
                                }
                            }
                        }
                    },
                    {"$sample": {"size": 1}},
                ]
            ).to_list(length=None)
        else:
            res = await self.chunithm_song_collection.aggregate(
                [
                    {"$match": {"charts": {"$elemMatch": {"level_value": decimal}}}},
                    {"$sample": {"size": 1}},
                ]
            ).to_list(length=None)
        if res:
            return ChuniSongData.from_dict(res[0])
        return None

    async def roll_chunithm_song_by_level_and_difficulty(
        self, level: str, difficulty: int
    ):
        """随机获取一首指定等级的中二歌曲"""
        if difficulty.int() != -1:
            res = await self.chunithm_song_collection.aggregate(
                [
                    {
                        "$match": {
                            "charts": {
                                "$elemMatch": {"difficulty": difficulty, "level": level}
                            }
                        }
                    },
                    {"$sample": {"size": 1}},
                ]
            ).to_list(length=None)
        else:
            res = await self.chunithm_song_collection.aggregate(
                [
                    {"$match": {"charts": {"$elemMatch": {"level": level}}}},
                    {"$sample": {"size": 1}},
                ]
            ).to_list(length=None)
        if res:
            return ChuniSongData.from_dict(res[0])
        return None

    async def query_maimai_arcade_by_keyword(self, keyword: str):
        """根据关键词查找舞萌机台"""
        cache_key = f"maimai_arcade_keyword_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        documents = []
        # 先从机厅名称里查找
        cur = self.maimai_arcade_collection.find({"arcadeName": {"$regex": keyword}})
        if cur:
            async for doc in cur:
                documents.append(doc)
        # 再在机厅地址里查找
        cur = self.maimai_arcade_collection.find({"address": {"$regex": keyword}})
        if cur:
            async for doc in cur:
                documents.append(doc)
        # 去重
        documents = deduplicate(documents)
        # 将结果转换成对象
        result = [ArcadeInfo.from_dict(doc) for doc in documents]
        self.cache.set(cache_key, result)
        return result

    async def query_chunithm_arcade_by_keyword(self, keyword: str):
        """根据关键词查找中二机台"""
        cache_key = f"chunithm_arcade_keyword_{keyword}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        documents = []
        # 先从机厅名称里查找
        cur = self.chunithm_arcade_collection.find({"arcadeName": {"$regex": keyword}})
        if cur:
            async for doc in cur:
                documents.append(doc)
        # 再在机厅地址里查找
        cur = self.chunithm_arcade_collection.find({"address": {"$regex": keyword}})
        if cur:
            async for doc in cur:
                documents.append(doc)
        # 去重
        documents = deduplicate(documents)
        # 将结果转换成对象
        result = [ArcadeInfo.from_dict(doc) for doc in documents]
        self.cache.set(cache_key, result)
        return result

    async def add_group_to_whitelist(self, group_id: int | str):
        """将群组加入白名单"""
        try:
            if isinstance(group_id, str):
                group_id = int(group_id)
            await self.group_whitelist_collection.insert_one({"group_id": group_id})
        except Exception as e:
            logger.error(f"添加群组到白名单时发生错误：{e}")

    async def remove_group_from_whitelist(self, group_id: int | str):
        """将群组移出白名单"""
        try:
            if isinstance(group_id, str):
                group_id = int(group_id)
            await self.group_whitelist_collection.delete_one({"group_id": group_id})
        except Exception as e:
            logger.error(f"从白名单中移出群组时发生错误：{e}")

    async def get_whitelist(self):
        """获取白名单列表"""
        try:
            res = await self.group_whitelist_collection.find({}).to_list()
            return [doc["group_id"] for doc in res]
        except Exception as e:
            logger.error(f"获取白名单列表时发生错误：{e}")
            return []

    async def add_user_to_blacklist(self, user_id: int | str):
        """将用户加入黑名单"""
        try:
            if isinstance(user_id, str):
                user_id = int(user_id)
            await self.user_blacklist_collection.insert_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"添加用户到黑名单时发生错误：{e}")

    async def remove_user_from_blacklist(self, user_id: int | str):
        """将用户移出黑名单"""
        try:
            if isinstance(user_id, str):
                user_id = int(user_id)
            await self.user_blacklist_collection.delete_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"从黑名单中移出用户时发生错误：{e}")

    async def get_blacklist(self):
        """获取黑名单列表"""
        try:
            res = await self.user_blacklist_collection.find({}).to_list()
            return [doc["user_id"] for doc in res]
        except Exception as e:
            logger.error(f"获取黑名单列表时发生错误：{e}")
            return []


connection = MongoDBConnect()
