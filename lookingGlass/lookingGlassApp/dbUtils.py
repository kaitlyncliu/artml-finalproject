from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_URI = os.environ['MONGO_URI']

client = MongoClient(MONGO_URI)

db = client['test']

def getConvoHistory(name):
    history = db.convos.find_one({"name": name})
    return history["msgHistory"]

def updateHistory(name, newMsgs):
    history = db.convos.find_one({"name": name})

    if history is not None:
        fullHistory = history['msgHistory']
        fullHistory.extend(newMsgs)
        newvalues = { "$set": { "msgHistory": fullHistory } }

        db.convos.update_one({"name": name}, newvalues)
    else:
        print("unable to find history")
        