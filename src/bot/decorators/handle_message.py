import asyncio
import functools
import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from src.logging.setup_logging import Log

logger = logging.getLogger(Log.BOT.value)


def handle_message(
    process_action: ChatAction = ChatAction.TYPING,
    finalize_action: ChatAction = ChatAction.TYPING,
):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            if not update.message or not update.message.text:
                logger.error("Message is empty.")
                return None
            url = update.message.text

            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=process_action,
            )

            logger.info(f"Downloading resource from {url}")
            task = asyncio.create_task(func(update, context, url=url, *args, **kwargs))

            while not task.done():
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id,
                    action=process_action,
                )
                await asyncio.sleep(4)

            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=finalize_action,
            )

            await update.message.delete()
            return task.result()

        return wrapper

    return decorator
