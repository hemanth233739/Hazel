from .. import on_message,HANDLER
from pyrogram import *
import asyncio, aiofiles.os
from MultiSessionManagement import clients_data,TgCallsClients,clients
from pytgcalls import filters as call_filters
import logging

async def StreamEndHandler(c,u):
  await c.mtproto_client.send_message('me',u)

c = PyTgCalls(clients[0])
c.start()
c.add_handler(StreamEndHandler)