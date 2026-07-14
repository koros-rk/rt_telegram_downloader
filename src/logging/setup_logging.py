import logging
import logging.handlers
from enum import Enum
from logging.handlers import TimedRotatingFileHandler


class Log(Enum):
    BOT = "bot"
    DOWNLOADER = "downloader"


def setup_logging():
    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
    )

    def make_handler(filename):
        handler = TimedRotatingFileHandler(
            "bot.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        handler.setFormatter(formatter)
        return handler

    bot_log = logging.getLogger(Log.BOT.value)
    bot_log.setLevel(logging.DEBUG)
    bot_log.addHandler(make_handler("bot.log"))

    downloader_log = logging.getLogger(Log.DOWNLOADER.value)
    downloader_log.setLevel(logging.DEBUG)
    downloader_log.addHandler(make_handler("downloader.log"))

    bot_log.info("Starting bot...")
    downloader_log.info("Starting downloader...")
