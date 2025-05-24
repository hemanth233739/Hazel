"""my love isn't joke."""
import logging
from art import *
from pyrogram import *
from clear import clear
import asyncio
from pytgcalls import PyTgCalls

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
      client.privilege, client.pytgcalls = privilege, pytgcalls_client
      await pytgcalls_client.start()
      clients_data[client.me.id] = {"client": client, "StreamingChats": {}, "pytgcalls_client": pytgcalls_client,"privilege": privilege}
      TgCallsClients.append(pytgcalls_client)
    except: clients.remove(client)
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
  
"you are my world"