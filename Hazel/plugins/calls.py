from pyrogram import *
from MultiSessionManagement import TgCallsClients
from pytgcalls import filters as fl
from pytgcalls.types import ChatUpdate
from .. import *

data = {}

@on_update(fl.chat_update(ChatUpdate.Status.INCOMING_CALL))
async def idk(c, u):
  global data
  await c.play(u.chat_id, "Assets/busy.mp3")
  if data.get(c.mtproto_client.me.id):
    data[c.mtproto_client.me.id].append(u.chat_id)
  else:
    data[c.mtproto_client.me.id] = [u.chat_id]

@on_update(fl.stream_end())
async def end_idk(c, u):
  global data
  app = c.mtproto_client
  if data.get(app.me.id) and (u.chat_id in data[app.me.id]):
    await c.leave_call(u.chat_id)
    data[app.me.id].remove(u.chat_id)
    if not data[app.me.id]:
      del data[app.me.id]