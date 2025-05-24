from .. import *
from pyrogram import *
from MultiSessionManagement import clients_data, clients

@on_message(filters.command('clients',prefixes=HANDLER) & filters.me)
async def fclients(c, m):
  n=await m.reply("`Processing...`")
  txt="![ℹ️](tg://emoji?id=5318840353510408444) **Clients informations**\n"
  for i in clients:
    if i.me:
      d=clients_data.get(i.me.id)
      txt+=f"""
•![👤](tg://emoji?id=5258011929993026890) - **{i.me.first_name}** (`{i.me.id}`)
 ![ℹ️](tg://emoji?id=4967518033061872209) **Client's id:** `{i.me.id}`
 ![🖱](tg://emoji?id=4970107898341360413) **Privilege:** {d.get('privilege')}\n"""
  txt+=f"\n![🌲](tg://emoji?id=5274182275704039686) **Total clients:** {len(clients)}"
  await n.delete()
  await m.reply(txt)

@app.on_message(filters.command('asudo',prefixes=HANDLER) & filters.me)
async def add_sudo(c,m):
  if not m.reply_to_message:
    if len(m.command) < 2: return await m.reply("Reply or enter id.")
    id = int(m.text.split(None, 1)[1])
  else: id = m.reply_to_message.from_user.id
  if id not in clients_data:
    return await m.reply("Client not found. You should add their session in OtherSessions in config.json or env.")
  elif (clients_data[id].get('privilege') == "sudo"):
    return await m.reply("They already has `sudo` privilege.")
  else:
    clients_data[id]["privilege"]="sudo"
    return await m.reply("Promoted.")
    
@app.on_message(filters.command('rsudo',prefixes=HANDLER) & filters.me)
async def remove_sudo(c,m):
  if not m.reply_to_message:
    if len(m.command) < 2: return await m.reply("Reply or enter id.")
    id = int(m.text.split(None, 1)[1])
  else: id = m.reply_to_message.from_user.id
  if id not in clients_data:
    return await m.reply("Client not found. You should add their session in OtherSessions in config.json or env.")
  elif (clients_data[id].get('privilege') != "sudo"):
    return await m.reply("They already don't have `sudo` privilege.")
  else:
    clients_data[id]["privilege"]="user"
    return await m.reply("Demoted.")