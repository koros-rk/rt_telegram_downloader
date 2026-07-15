import asyncio
import os

from aiohttp import web
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler

from src.bot.filters.instagram_url_filter import InstagramFilter
from src.bot.filters.tiktok_url_filter import TikTokFilter
from src.bot.filters.video_url_filter import VideoUrlFilter
from src.bot.filters.youtube_url_filter import YoutubeFilter
from src.bot.handlers.video_url_handler import video_url_handler

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAB_BOT_TOKEN")
application = Application.builder().token(BOT_TOKEN).build()


async def health_check(request):
    return web.Response(text="OK")


async def start_dummy_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()


async def bootstrap_bot():
    async with application as app:
        app.add_handler(MessageHandler(VideoUrlFilter(), video_url_handler))

        await start_dummy_server()

        await application.start()
        await application.updater.start_polling()
        await asyncio.Event().wait()
        await application.updater.stop()
        await application.stop()
