from urllib.parse import urlparse

from telegram.ext.filters import MessageFilter

from src.downloader.video.is_supported import is_supported


class VideoUrlFilter(MessageFilter):
    domains = {
        # TikTok
        "tiktok.com",
        "www.tiktok.com",
        "m.tiktok.com",
        "vm.tiktok.com",
        "vt.tiktok.com",
        # YouTube
        "youtube.com",
        "www.youtube.com",
        # Instagram
        "instagram.com",
        "www.instagram.com",
    }

    def __init__(self):
        super().__init__()

    @classmethod
    def is_supported_url(cls, url):
        try:
            url = urlparse(url)

            if url.scheme not in ("http", "https"):
                return False

            if url.netloc.casefold() not in cls.domains:
                return False

            return True
        except Exception:
            return False

    def filter(self, message):
        if url := message.text:
            is_valid_url = self.is_supported_url(url)
            is_downloadable = is_supported(url)
            return is_valid_url and is_downloadable
        return False
