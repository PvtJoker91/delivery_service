from abc import ABC, abstractmethod


class BaseCacheStorage(ABC):
    @abstractmethod
    async def set_data(self, key, data, expiration):
        ...

    @abstractmethod
    async def get_data(self, key):
        ...
