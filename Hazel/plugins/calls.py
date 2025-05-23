from .. import *
from pyrogram import *
from pytgcalls import filters as fl
from pytgcalls.types import ChatUpdate
from MultiSessionManagement import *

cl = TgCallsClients[0]
@cl.on_update(fl.chat_update(ChatUpdate.Status.INCOMING_CALL))
async def idk(c,u):
  await c.mtproto_client.send_message(u.chat.id,"hmm?")
  await c.play(u.chat.id,"Assets/busy.mp3")