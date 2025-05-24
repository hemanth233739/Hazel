import logging
from art import *
from pyrogram import *
from clear import clear
import asyncio
from pytgcalls import PyTgCalls
import logging

log = logging.getLogger(__name__)
clients, clients_data = [],{}
TgCallsClients = []

def add_client(client):
  global clients,clients_data
  if client not in clients:
    clients.append(client)

async def start_all():
  global clients_data,TgCallsClients
  from Hazel import bot,nexbot
  await bot.start()
  await nexbot.start()
  for client in clients:
    try:
      privilege = f"{'sudo' if client == clients[0] else 'user'}"
      await client.start()
      pytgcalls_client = PyTgCalls(client)
      await pytgcalls_client.start()
      client.privilege, client.pytgcalls = privilege, pytgcalls_client      
      clients_data[client.me.id] = {"client": client, "StreamingChats": {}, "pytgcalls_client": pytgcalls_client,"privilege": privilege}
      TgCallsClients.append(pytgcalls_client)
    except Exception as e:
      clients.remove(client)
      log.error(e)
  from Essentials.vars import AutoJoinChats, Support
  for app in clients:
    for i in AutoJoinChats:
      try: await app.join_chat(i)
      except: pass
  z,x,c=clear(),print(text2art("HazelUB"), end=""),logging.info("You're all set!")
  try: await clients[0].send_message(Support,"Up!")
  except: pass
  from personal.UpdateWaitingDays import UpdateWaitingDays
  asyncio.create_task(UpdateWaitingDays(clients[0]))
  await idle()