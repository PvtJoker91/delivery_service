from motor.motor_asyncio import AsyncIOMotorClient

from app.settings.config import settings

mongo_client = AsyncIOMotorClient(
    settings.mongo.mongodb_connection_url,
    serverSelectionTimeoutMS=3000,
)


def init_mongodb_client():
    return mongo_client
