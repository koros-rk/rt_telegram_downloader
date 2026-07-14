import asyncio
import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from src.bot.decorators.handle_error import handle_errors
from src.downloader.video.downloader import video_downloader
from src.logging.setup_logging import Log

logger = logging.getLogger(Log.BOT.value)


@handle_errors()
async def url_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        logger.error("Message is empty.")
        return
    url = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.UPLOAD_VIDEO,
    )

    logger.info(f"Downloading resource from {url}")
    task = asyncio.create_task(video_downloader(url))

    while not task.done():
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.UPLOAD_VIDEO,
        )
        await asyncio.sleep(4)

    video = await task
    logger.info("Download completed.")

    logger.info(f"Sending resource to {update.effective_chat.id}.")
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        filename="video.mp4",
        video=video,
    )
    logger.info("Resource sent.")
