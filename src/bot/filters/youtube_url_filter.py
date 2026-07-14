from urllib.parse import urlparse

from telegram.ext.filters import MessageFilter


class YoutubeFilter(MessageFilter):
    def __init__(self):
        self.domains = {
            "youtube.com",
            "www.youtube.com",
        }
        super().__init__()

    def filter(self, message):
        try:
            if message.text is None:
                return False
            url = urlparse(message.text)

            if url.scheme not in ("http", "https"):
                return False

            if not url.path.startswith("/shorts"):
                return False

            if url.netloc.lower() not in self.domains:
                return False

            return True
        except Exception:
            return False
