from .. import on_message,HANDLER
from pyrogram import *
import asyncio, aiofiles.os
from MultiSessionManagement import clients_data,TgCallsClients,clients
from pytgcalls import filters as call_filters
import logging

async def StreamEndHandler(c,u):
  logging.info(u)

TgCallsClients[0].add_handler(StreamEndHandler, call_filters.stream_end())
