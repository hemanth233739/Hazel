from .. import *
from pyrogram import *
import asyncio, aiofiles.os
from MultiSessionManagement import *

async def WaitForFile(f):
  return await aiofiles.os.path.exists(f) or await asyncio.sleep(0.1) or await WaitForFile(f)

@on_message(filters.command('stream',prefixes=HANDLER)&filters.me)
async def stream_func(c,m):
  if len(m.command) < 2:
    return await m.reply("I'll stream, but from where? Give me chat's id.")
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  chat=str(m.command[1])
  try: chat = await c.get_chat(chat)
  except Exception as e: return await m.reply(f"Failed: {e}.")
  if chat.type not in [enums.ChatType.GROUP,enums.ChatType.SUPERGROUP]:
    return await m.reply('Please give only group/supergroup id.')
  file_name = f"chat{chat.id}-recording.mp3"
  try: await aiofiles.os.remove(file_name)
  except: pass
  await pytgcalls_client.record(chat.id,file_name)
  await WaitForFile(file_name)
  try:
    await pytgcalls_client.play(m.chat.id,file_name)
    await m.reply(f"Streaming started! All audio from {chat.title}'s vc also can be heared from here. Use .sstream **on this chat** to stop streaming.")
  except Exception as e: return await m.reply(f"Failed to stream the audio: {e}")
  um = await c.listen(m.chat.id,m.from_user.id,filters=(filters.command('sstream',prefixes=HANDLER)))
  if um.command[0] == "sstream":
    await um.reply_audio(file_name,caption="Recording.")
    await pytgcalls_client.leave_call(chat.id)
    await pytgcalls_client.leave_call(m.chat.id)
    await um.reply("Streaming has been stopped.")
    await aiofiles.os.remove(file_name)