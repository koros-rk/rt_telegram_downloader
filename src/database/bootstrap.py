import logging
import os

from pymongo import MongoClient
from pymongo.database import Database
from functools import lru_cache
from dotenv import load_dotenv

from src.logging.setup_logging import Log

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

MongoDBClient = MongoClient(DATABASE_URL)
logger = logging.getLogger(Log.BOT.value)


@lru_cache
def get_client() -> MongoClient:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

    client = MongoClient(DATABASE_URL)
    return client


def get_database() -> Database:
    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME is not set")

    client = get_client()
    return client[DATABASE_NAME]


def ping_database() -> bool:
    try:
        client = get_client()
        client.admin.command("ping")
        return True
    except Exception:
        logger.exception("Database connection failed")
        return False


def close_client() -> None:
    logger.info("Closing database connection")
    get_client().close()


if __name__ == "__main__":
    client = get_client()
    db = client["test_database"]
    print(db.list_collection_names())
    for doc in db["downloads"].find({}):
        print(doc)
