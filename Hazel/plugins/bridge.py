import numpy as np
from pytgcalls import filters as call_filter
from pytgcalls.types import Device, Direction, ExternalMedia, RecordStream, MediaStream, StreamFrames
from pytgcalls.types.raw import AudioParameters
from Hazel import on_message, HANDLER
from pyrogram import filters

func = {}

@on_message(filters.command('bridge',prefixes=HANDLER) & filters.me)
async def bridge_func(app,m):
  global func
  if func:
    return await m.reply("Already this command is running somewhere. Please use .sbridge to end it.")
  elif len(m.command) < 2:
    return await m.reply("Okay, I'll bridge. But from where?")
  chat = m.command[1]
  try: chat = await app.get_chat(chat)
  except: return await m.reply("Cannot find the chat.")
  call_py = app.pytgcalls
  AUDIO_PARAMETERS = AudioParameters(bitrate=48000, channels=2)
  chat_ids = [m.chat.id,chat.id]
  for chat_id in chat_ids:
    await call_py.play(chat_id,MediaStream(ExternalMedia.AUDIO,AUDIO_PARAMETERS))
    await call_py.record(chat_id,RecordStream(True,AUDIO_PARAMETERS))
  func["chat_ids"] = chat_ids
  await m.reply("Done.")
  async def audio_data(_, update):
    forward_chat_ids = [x for x in chat_ids if x != update.chat_id]
    mixed_output = np.zeros(
      len(update.frames[0].frame) // 2,
      dtype=np.int16,
    )
    for frame_data in update.frames:
      source_samples = np.frombuffer(frame_data.frame, dtype=np.int16)
      mixed_output[:len(source_samples)] += source_samples
    mixed_output //= max(len(update.frames), 1)
    mixed_output = np.clip(mixed_output, -32768, 32767)
    for f_chat_id in forward_chat_ids:
      await call_py.send_frame(f_chat_id,Device.MICROPHONE,mixed_output.tobytes())
  await call_py.add_handler(audio_data, call_filter.stream_frame(Direction.INCOMING,Device.MICROPHONE))
  func["func"] = audio_data