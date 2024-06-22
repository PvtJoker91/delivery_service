from motor.motor_asyncio import AsyncIOMotorClient

from app.settings.config import settings


def init_mongodb_client():
    return AsyncIOMotorClient(
        settings.mongo.mongodb_connection_uri,
        serverSelectionTimeoutMS=3000,
    )
