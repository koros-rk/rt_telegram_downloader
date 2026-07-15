import asyncio
from src.bot.bootstrap import bootstrap_bot
from src.database.bootstrap import ping_database, close_client
from src.logging.setup_logging import setup_logging

if __name__ == "__main__":
    setup_logging()
    if  not ping_database():
        exit(1)
    asyncio.run(bootstrap_bot())
    close_client()
