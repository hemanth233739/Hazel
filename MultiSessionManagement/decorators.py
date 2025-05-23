from pyrogram import *
"""I love her. Tbh"""

def on_message(filters=None, group=0):
  def decorator(func):
    from . import clients
    for i in clients:
      i.on_message(filters, group=group)(func)
    return func
  return decorator
  
def on_update(*args, **kwarg): #PyTgCalls decorator...
  def decorator(func):
    from . import TgCallsClients
    for i in TgCallsClients:
      i.on_update(*args,**kwargs)(func)
    return func
  return decorator