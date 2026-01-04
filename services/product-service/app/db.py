from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import settings

client = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_db]

def products_collection():
    return db["products"]
