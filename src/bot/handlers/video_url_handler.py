import logging

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.bot.decorators.handle_cache import handle_cache
from src.bot.decorators.handle_error import handle_errors
from src.bot.decorators.handle_message import handle_message
from src.bot.utils.get_message_caption import get_message_caption
from src.database.entities.record import FileType
from src.downloader.video.downloader import video_downloader
from src.logging.setup_logging import Log

logger = logging.getLogger(Log.BOT.value)


@handle_errors()
@handle_cache(file_type=FileType.VIDEO)
@handle_message(
    process_action=ChatAction.RECORD_VIDEO,
    finalize_action=ChatAction.UPLOAD_VIDEO,
)
async def video_url_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    url: str,
    file_ids: list[str] | None = None,
):
    if file_ids:
        logger.info(f"Resource {url} found in cache.")
        video = file_ids[0]
    else:
        logger.info(f"Resource {url} is not in cache. Downloading...")
        video = await video_downloader(url)

    logger.info(f"Sending resource to {update.effective_chat.id}.")
    message = await context.bot.send_video(
        video=video,
        chat_id=update.effective_chat.id,
        caption=get_message_caption(url),
        parse_mode=ParseMode.HTML,
    )
    logger.info(f"Resource {message.video.file_id} sent.")

    return url, [message.video.file_id]
