from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = False
MONGO_URI = os.environ['MONGO_URI']

client = MongoClient(MONGO_URI)

db = client['test']

def getConvoHistory(name):
    history = db.convos.find_one({"name": name})

    if DEBUG: print("Previous history: ", history)

    if history is not None:
        return history.get("msgHistory", None)
    else:
        return None

def updateHistory(name, newMsgs):
    history = db.convos.find_one({"name": name})

    if DEBUG: print(f"Updating history for {name} with: ", history)

    if history is not None:
        fullHistory = history.get("msgHistory", list())
        fullHistory.extend(newMsgs)
        newvalues = { "$set": { "msgHistory": fullHistory } }

        db.convos.update_one({"name": name}, newvalues)
    else:
        newHistory = list()
        newHistory.extend(newMsgs)
        newvalues = { "$set": { "msgHistory": newHistory } }

        db.convos.insert_one({"name": name}, newvalues)
        