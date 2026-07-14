import asyncio
from src.bot.bootstrap import bootstrap
from src.logging.setup_logging import setup_logging

if __name__ == "__main__":
    setup_logging()
    asyncio.run(bootstrap())
