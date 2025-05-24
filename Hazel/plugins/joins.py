from .. import *
from pyrogram import *

@on_message(filters.command(['join','leave'], prefixes=HANDLER) & filters.me)
async def joins_func(app,m):
  if (len(m.command) < 2 and m.command[0]=='leave' and m.chat.type not in [enums.ChatType.BOT,enums.ChatType.PRIVATE]):
    await app.leave_chat(m.chat.id)
  elif (len(m.command) < 2):
    return await m.reply(f'need username/link to {m.command[0]}.')
  link = m.text.split(" ")[1]
  if m.command[0]=='join':
    try:
      await app.join_chat(link)
      await m.reply("Okay, you've been successfully joined in.")
    except: return await m.reply('Failed. (Probably this is an issue with the link you provied.)')
  else:
    try:
      await m.reply('leaved.')
      await app.leave_chat(link)     
    except: return await m.reply('Failed. (Probably this is an issue with the link you provied.)')
      
MOD_NAME = "joins"
MOD_HELP = ".join <link/username> - to join there\n.leave <link/username/blank> - pass chat link or try in a group to leave from there."