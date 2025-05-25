from Hazel import HANDLER, on_message
from pyrogram import filters
import os
import requests
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

@on_message(filters.command(["song", "video"], prefixes=HANDLER) & filters.me)
async def youtube(app, message):
  if len(message.text.split()) < 2:
    return await message.reply("Provide a song/video name or YouTube link.")
  query = " ".join(message.command[1:])
  is_video = message.command[0].lower() == "video" 
  try:
    if query.startswith(("www.youtube", "http://", "https://")):
      link = query
      with YoutubeDL({'quiet': True, 'cookiefile': 'cookies.txt'}) as ydl:
        info = ydl.extract_info(link, download=False)
        title = info.get("title", "Unknown Title")
        thumbnail = info.get("thumbnail")
        duration = info.get("duration", 0)
    else:
      results = YoutubeSearch(query, max_results=1).to_dict()
      if not results:
        return await message.reply("No results found.")
      link = f"https://youtube.com{results[0]['url_suffix']}"
      title = results[0]["title"]
      thumbnail = results[0]["thumbnails"][0]
      duration = results[0]["duration"]
    thumb_name = f"{title.replace('/', '_')}.jpg"
    if thumbnail:
      thumb = requests.get(thumbnail, allow_redirects=True)
      if thumb.status_code == 200:
        with open(thumb_name, "wb") as f:
          f.write(thumb.content)
      else:
        thumb_name = None
    msg = await message.reply("📥 Downloading...")
    ydl_opts = {
      "format": "best" if is_video else "bestaudio[ext=m4a]",
      "cookiefile": "cookies.txt",
      "outtmpl": f"downloads/%(title)s.%(ext)s"
    }    
    try:
      with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        media_file = ydl.prepare_filename(info_dict)    
      secmul, dur, dur_arr = 1, 0, str(duration).split(":")
      for i in range(len(dur_arr) - 1, -1, -1):
        dur += int(float(dur_arr[i])) * secmul
        secmul *= 60
      
      await msg.edit("📤 Uploading...")
      if is_video:
        await message.reply_video(
          media_file,
          thumb=thumb_name,
          caption=f"**{title}**",
          duration=dur
        )
      else:
        await message.reply_audio(
          media_file,
          thumb=thumb_name,
          title=title,
          caption=f"{title}",
          duration=dur
        )      
      await msg.delete()
      if os.path.exists(media_file):
        os.remove(media_file)
      if thumb_name and os.path.exists(thumb_name):
        os.remove(thumb_name)
    except Exception as e:
      await msg.edit(f"Error downloading/uploading: {e}")
  except Exception as e:
    await message.reply(f"Error: {e}")

MOD_NAME = "YouTube"
MOD_HELP = ".song <text/link> - To download the song from YouTube.\n.video <text/link> - To download the video from YouTube."