from urllib.parse import urlparse

from telegram.ext.filters import MessageFilter


class TikTokFilter(MessageFilter):
    def __init__(self):
        self.domains = {
            "tiktok.com",
            "www.tiktok.com",
            "m.tiktok.com",
            "vm.tiktok.com",
            "vt.tiktok.com",
        }
        super().__init__()

    def filter(self, message):
        try:
            if message.text is None:
                return False
            url = urlparse(message.text)

            if url.scheme not in ("http", "https"):
                return False

            if url.netloc.lower() not in self.domains:
                return False

            return True
        except Exception:
            return False
