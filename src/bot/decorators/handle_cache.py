import asyncio
import functools
import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from src.database.bootstrap import ping_database
from src.database.repositories.downloads import DownloadsRepository, FileType
from src.logging.setup_logging import Log

logger = logging.getLogger(Log.BOT.value)


def handle_cache(file_type: FileType):
    repository = DownloadsRepository()

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            if not ping_database():
                logger.error("Database connection failed.")
                return func(update, context, *args, **kwargs)

            if not update.message or not update.message.text:
                logger.error("Message is empty.")
                return
            url = update.message.text
            user_id = update.message.from_user.id

            record = repository.get(url=url)
            file_ids = record.file_ids if record else None

            url, ids = await func(update, context, file_ids=file_ids, *args, **kwargs)

            if not record:
                repository.add(
                    url=url,
                    file_ids=ids,
                    file_type=file_type,
                    user_id=str(user_id),
                )

            return url, ids

        return wrapper

    return decorator
