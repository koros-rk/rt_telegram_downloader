import logging

import yt_dlp
import os
import asyncio
from functools import partial

from src.downloader.errors.file_too_large import FileTooLarge
from src.downloader.errors.url_not_supported import UrlNotSupported
from src.downloader.video.get_config import build_ydl_opts, TELEGRAM_MAX_MB
from src.downloader.video.is_supported import is_supported
from src.logging.setup_logging import Log

logger = logging.getLogger(Log.DOWNLOADER.value)


def _download_sync(url: str, max_size_mb: int) -> bytes:
    logger.info(f"Starting download: url={url}.")
    opts = build_ydl_opts(max_size_mb)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        logger.info(f"Prepared filename: {filepath}")

        base, _ = os.path.splitext(filepath)
        mp4_path = base + ".mp4"
        if os.path.exists(mp4_path):
            filepath = mp4_path

        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > max_size_mb:
            logger.info(f"File exceeded max file size: {max_size_mb}.")
            os.remove(filepath)
            raise FileTooLarge(max_size_mb)

        with open(filepath, "rb") as f:
            video_bytes = f.read()

        os.remove(filepath)
        logger.info(f"Downloaded resource resolved. Temporary file deleted.")
        return video_bytes


async def video_downloader(url: str) -> bytes:
    if not is_supported(url):
        raise UrlNotSupported(url)

    loop = asyncio.get_running_loop()
    func = partial(_download_sync, url, TELEGRAM_MAX_MB)
    return await loop.run_in_executor(None, func)
