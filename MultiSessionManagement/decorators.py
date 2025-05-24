from pyrogram import *
def on_message(filters=None, group=0):
  def decorator(func):
    from . import clients
    for i in clients:
      i.on_message(filters, group=group)(func)
    return func
  return decorator
  
def on_update(*args):
  def decorator(func):
    from . import TgCallsClients
    for i in TgCallsClients:
      i.on_update(*args)(func)
    return func
  return decorator  