import logging
import os

from yt_dlp.networking.impersonate import ImpersonateTarget

from src.logging.setup_logging import Log

logger = logging.getLogger(Log.DOWNLOADER.value)


TELEGRAM_MAX_MB = 50
TELEGRAM_MAX_BYTES = TELEGRAM_MAX_MB * 1024 * 1024

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def build_ydl_opts(
    max_size_mb: int = TELEGRAM_MAX_MB, directory: str = DOWNLOAD_DIR
) -> dict:
    max_bytes = max_size_mb * 1024 * 1024

    return {
        "format": (
            "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]"
            "/best[ext=mp4][height<=720]"
            "/bestvideo[height<=720]+bestaudio"
            "/best[height<=720]"
            "/best"
        ),
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
        "outtmpl": os.path.join(directory, "%(extractor)s_%(id)s.%(ext)s"),
        "restrictfilenames": True,
        "socket_timeout": 30,
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 3,
        "file_access_retries": 3,
        "ratelimit": 2 * 1024 * 1024,
        "throttledratelimit": 100_000,
        "sleep_interval_requests": 1,
        "sleep_interval": 1,
        "max_sleep_interval": 5,
        "impersonate": ImpersonateTarget.from_str("chrome"),
        "quiet": True,
        "no_warnings": False,
        "noplaylist": True,
        "max_filesize": max_bytes,
        "overwrites": True,
        "concurrent_fragment_downloads": 4,
        "logger": logger,
    }
