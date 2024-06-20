from abc import ABC, abstractmethod


class BaseCacheDB(ABC):
    @abstractmethod
    async def set_data(self, key, data, expiration):
        ...

    @abstractmethod
    async def get_data(self, key):
        ...
