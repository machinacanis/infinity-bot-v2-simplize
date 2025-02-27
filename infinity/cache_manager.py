import asyncio
import threading

from cachetools import LRUCache

# code from github.com/machinacanis/kikaiken-bot

class CacheManager:
    """
    缓存管理模块
    """

    def __init__(self, tag_name: str, max_size: int):
        self.tag_name = tag_name
        self.lock = threading.Lock()
        self.cache = LRUCache(maxsize=max_size)
        self.cache_size = max_size

    def set(self, key: str, value: any):
        with self.lock:
            self.cache[key] = value

    def get(self, key: str):
        with self.lock:
            return self.cache.get(key)

    async def aset(self, key: str, value: any):
        """异步版本，疑似存在问题，不建议使用"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.set, key, value)

    async def aget(self, key: str):
        """异步版本，疑似存在问题，不建议使用"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get, key)
