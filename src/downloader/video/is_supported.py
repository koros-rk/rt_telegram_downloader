import yt_dlp.utils

from src.downloader.video.get_config import build_ydl_opts


def is_supported(url: str, max_size_mb: int, directory: str) -> bool:
    opts = build_ydl_opts(max_size_mb, directory)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            ydl.extract_info(url, download=False)
            return True
        except yt_dlp.utils.DownloadError as e:
            if "Unsupported URL" in str(e):
                return False
            return True
