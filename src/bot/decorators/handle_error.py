import functools
import logging

import telegram.error
from telegram import Update
from telegram.ext import ContextTypes

from src.downloader.errors.file_too_large import FileTooLarge
from src.downloader.errors.url_not_supported import UrlNotSupported
from src.logging.setup_logging import Log

logger = logging.getLogger(Log.BOT.value)

DEFAULT_ERROR_MESSAGE = "Unable to process your message. Please try again later."
UNSUPPORTED_FORMAT_MESSAGE = "Unsupported resource. Please try another one."
FILE_TOO_LARGE_MESSAGE = "Resource file is too large. Please try another one."
TIMEOUT_MESSAGE = "Resource download timed out. Please try again later."


async def send_tg_message(update: Update, message: str):
    try:
        if update.effective_message:
            await update.effective_message.reply_text(message)
        elif update.effective_chat:
            await update.effective_chat.send_message(message)
    except Exception:
        logger.exception("Failed to send error message to user for handler")


def handle_errors():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                return await func(update, context)
            except telegram.error.TimedOut as e:
                await send_tg_message(update, TIMEOUT_MESSAGE)
                logger.info(e.message)
                return None
            except FileTooLarge as e:
                logger.info(e.message)
                await send_tg_message(update, FILE_TOO_LARGE_MESSAGE)
                return None
            except UrlNotSupported as e:
                logger.info(e.message)
                await send_tg_message(update, UNSUPPORTED_FORMAT_MESSAGE)
                return None
            except Exception:
                logger.exception("Unhandled exception in handler %s", func.__name__)
                await send_tg_message(update, DEFAULT_ERROR_MESSAGE)
                return None

        return wrapper

    return decorator
