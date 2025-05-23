from .. import *
from pyrogram import *
import asyncio, aiofiles.os
from MultiSessionManagement import *

async def WaitForFile(f):
  return await aiofiles.os.path.exists(f) or await asyncio.sleep(0.01) or await WaitForFile(f)

@on_message(filters.command('stream', prefixes=HANDLER) & filters.me)
async def stream_func(c,m):
  global clients_data
  if m.chat.id in clients_data[c.me.id]["StreamingChats"]:
    return await m.reply("Already a stream is ongoing on this chat. You have to stop it by using `.sstream` to make an another stream.")
  if len(m.command) < 2:
    return await m.reply("I'll stream, but from where? Give me chat's id.")
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  chat = str(m.command[1])
  try: chat = await c.get_chat(chat)
  except Exception as e: return await m.reply(f"Failed: {e}.")
  if chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
    return await m.reply('Please give only group/supergroup id.')
  file_name = f"chat{chat.id}-recording.mp3"
  try: await aiofiles.os.remove(file_name)
  except: pass
  await pytgcalls_client.record(chat.id, file_name)
  await WaitForFile(file_name)
  try:
    await pytgcalls_client.play(m.chat.id, file_name)
    await m.reply(f"Streaming started! Audio from {chat.title}'s VC is being streamed here. Use .sstream **in this chat** to stop the streaming.")
  except Exception as e:
    return await m.reply(f"Failed to stream the audio: {e}")
  if "StreamingChats" not in clients_data[c.me.id]:
    clients_data[c.me.id]["StreamingChats"] = {}
  clients_data[c.me.id]["StreamingChats"][m.chat.id] = {"source": chat.id,"file": file_name}

@on_message(filters.command('sstream', prefixes=HANDLER) & filters.me)
async def stop_stream(c,m):
  global clients_data
  try:streaming_data = clients_data[c.me.id]["StreamingChats"][m.chat.id]
  except KeyError: return await m.reply("Nothing streaming in this chat.")
  if not streaming_data:
    return await m.reply("Nothing streaming in this chat tbh.")
  source = streaming_data["source"]
  file_name = streaming_data["file"]
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  await pytgcalls_client.leave_call(source)
  await pytgcalls_client.leave_call(m.chat.id)
  await m.reply("Streaming has been stopped.")
  if not await aiofiles.os.path.exists(file_name):
    return await m.reply("Streaming file is not found so cannot send the recording.")
  await m.reply_audio(file_name)
  await aiofiles.os.remove(file_name)
  del clients_data[c.me.id]["StreamingChats"][m.chat.id]