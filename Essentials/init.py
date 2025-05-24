import logging
import json
from art import *
from clear import clear
import ast
log = logging.getLogger(__name__)

credits = """Cretor: Otazuki
Github: https://github.com/DevsBase/HazelUB
"""

class Init:
  def __init__(self):
    import os
    clear()
    print(text2art("HazelUB"), end="")
    print(credits)
    DefaultKeys = ['API_ID', 'API_HASH', 'PYROGRAM_SESSION', 'BOT_TOKEN', 'MONGO_DB_URL']
    OtherKeys = ['quick_start', 'OtherSessions']
    data,config={}, {}
    if os.path.exists("config.json"):
      try:
        with open("config.json") as f:
          config = json.load(f)
      except Exception as e:
        log.error("Failed to load config.json")
        log.error(str(e))
    for key in DefaultKeys:
      if not (config.get(key) or os.getenv(key)):
        try:
          i = input(f"Cannot find {key} in config.json & env. Enter: ")
          if not i: Init()
        except EOFError:
          log.error("Some keys are missing. Please add them in config.json or as a ENV.")
          exit()
        data[key] = config.get(key) or os.getenv(key) or i
      else: data[key] = config.get(key) or os.getenv(key)
    for k in OtherKeys:
      data[k] = config.get(k)
      if k == "OtherSessions":
        data[k] = config.get(k,[]) or ast.literal_eval(os.getenv(k) or "None")
        if not isinstance(data[k], list): data[k]=[]
    try:
      if not (config.get('quick_start')):
        print("Please check values below:")
        for key in DefaultKeys:
          print(f"{key}: {repr(data[key])}")
        confirm = input("Are these correct? (y/n): ").strip().lower()
      else: confirm='y'
    except EOFError:
      log.info("EOF detected. Continuing with y.")
      confirm="y"
    if confirm != "y":
      for key in DefaultKeys:
        try:
          data[key] = input(f"Enter {key}: ").strip()
        except EOFError:
          log.error(f"EOF detected while entering {key}. Exiting.")
          exit()
    self.output = {
      "API_ID": int(data['API_ID']),
      "API_HASH": data['API_HASH'],
      "PYROGRAM_SESSION": data['PYROGRAM_SESSION'],
      "BOT_TOKEN": data['BOT_TOKEN'],
      "OtherSessions": data.get('OtherSessions')
    }
    if len(data.get('OtherSessions')) > 5:
      raise ValueError("You cannot add more than 5 sessions.")