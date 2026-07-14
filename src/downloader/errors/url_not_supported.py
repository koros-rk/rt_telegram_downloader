class UrlNotSupported(Exception):
    def __init__(self, url: str):
        self.url = url
        self.message = f"Resource [{url}] is not supported"
        super().__init__(self.message)
