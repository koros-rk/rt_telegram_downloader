from telegram.helpers import escape_markdown


def get_message_caption(source_url: str):
    return f"<a href='{escape_markdown(source_url)}'>source</a> {escape_markdown("✤")} <a href='{escape_markdown('https://t.me/rt_downloader_bot')}'>via</a>"
