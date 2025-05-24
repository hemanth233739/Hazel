from pyrogram import *
from MultiSessionManagement import TgCallsClients
from pytgcalls import filters as fl
from pytgcalls.types import ChatUpdate
from .. import *

@TgCallsClients[0].on_update(fl.chat_update(ChatUpdate.Status.INCOMING_CALL))
async def idk(c,u):
  await c.mtproto_client.send_message(u.chat_id,"Um?")
  await c.play(u.chat_id,"Assets/busy.mp3")