from .. import *
from pyrogram import filters
import requests
from datetime import datetime

def ping_website():
  try:
    url = "https://google.com"
    response = requests.get(url)
    return f"{response.elapsed.total_seconds() * 1000:.2f}ms" if response.ok else f"Failed to ping {url}"
  except requests.ConnectionError: return f"» Failed to connect to {url}"

@on_message(filters.command("ping", prefixes=HANDLER) & filters.user('me'))
async def ping_pong(client, message):
  uptime = datetime.now() - start_time
  await message.reply_text(f"» Pᴏɴɢ! Rᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ: {ping_website()}\n» Uᴘᴛɪᴍᴇ: {uptime.seconds // 3600}h {(uptime.seconds // 60) % 60}m {uptime.seconds % 60}s")