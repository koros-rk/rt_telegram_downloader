from urllib.parse import urlparse

from telegram.ext.filters import MessageFilter


class InstagramFilter(MessageFilter):
    def __init__(self):
        self.domains = {
            "instagram.com",
            "www.instagram.com",
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
