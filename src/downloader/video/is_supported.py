import yt_dlp.utils

from src.downloader.video.downloader import TELEGRAM_MAX_MB, DOWNLOAD_DIR
from src.downloader.video.get_config import build_ydl_opts


def is_supported(url: str, max_size_mb: int = TELEGRAM_MAX_MB, directory: str = DOWNLOAD_DIR) -> bool:
    opts = build_ydl_opts(max_size_mb, directory)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            ydl.extract_info(url, download=False)
            return True
        except yt_dlp.utils.DownloadError as e:
            return False
