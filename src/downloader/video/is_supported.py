import yt_dlp.utils

from src.downloader.video.get_config import build_ydl_opts


def is_supported(url: str) -> bool:
    opts = build_ydl_opts()

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            ydl.extract_info(url, download=False)
            return True
        except yt_dlp.utils.DownloadError as e:
            return False
