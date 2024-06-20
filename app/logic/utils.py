import bcrypt
import httpx
import pickle

from app.domain.exceptions.users import PasswordValidationException
from app.domain.constants import CACHE_EXCHANGE_NAME, EXCHANGE_URL
from app.infra.cache.base import BaseCacheDB
from app.infra.exceptions.http import HTTPRequestException


async def get_rub_exchange_rates(cache_db: BaseCacheDB):
    """
    Получает курс обмена рубля из кэша или удаленного API.
    Args:
        cache_db (BaseCacheDB): Объект базы данных для кэширования данных.
    Returns:
        dict: Данные курса обмена рубля.
    Raises:
        HTTPRequestException: Если запрос к удаленному API не удался.
    """
    cached_data = await cache_db.get_data(CACHE_EXCHANGE_NAME)
    if cached_data:
        data = pickle.loads(cached_data)
    else:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(EXCHANGE_URL)
        except httpx.HTTPError:
            raise HTTPRequestException(url=EXCHANGE_URL)
        data = res.json()
        data_bytes = pickle.dumps(data)
        await cache_db.set_data(CACHE_EXCHANGE_NAME, data_bytes, 3600)
    return data


def calculate_cost(price: float, weight: float, exchange_rate: float) -> float:
    """
    Рассчитывает стоимость товара на основе цены, веса и курса обмена.
    Args:
        price (float): Цена товара.
        weight (float): Вес товара.
        exchange_rate (float): Курс обмена валюты.
    Returns:
        float: Рассчитанная стоимость товара.
    """
    return (weight * 0.5 + price * 0.01) * exchange_rate


def is_nullable(cond: bool):
    """
    Определяет, следует ли возвращать None на основе условия.
    Args:
        cond (bool): Условие для проверки.
    Returns:
        None: Если условие истинно.
        bool: Если условие ложно.
    """
    return None if cond else not None


def hash_password(password: str) -> bytes:
    """
    Хэширует пароль с использованием библиотеки bcrypt.

    Args:
        password (str): Пароль для хэширования.

    Returns:
        bytes: Захэшированный пароль.
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Проверяет пароль на соответствие захэшированному паролю.
    Args:
        password (str): Пароль для проверки.
        hashed_password (bytes): Захэшированный пароль для сравнения.
    Returns:
        bool: True, если пароль действителен, иначе False.
    Raises:
        PasswordValidationException: Если пароль не прошел проверку.
    """
    is_valid = bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
    if not is_valid:
        raise PasswordValidationException
    return is_valid
