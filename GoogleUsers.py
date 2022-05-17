import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
# mongo_key = os.environ.get("mongo_key")
connection_string = os.environ.get("connection_string")

def getMongoClient():
    return MongoClient(connection_string)

mongo_client = getMongoClient()
db = mongo_client.Users
users_collection = db['UsersDetails']
history_collection = db['UsersHistory']

def removeUsersCollection():
    users_collection.delete_many({})
# removeUsersCollection()
# history_collection.delete_many({})

def addUser(googleId, token):
    if isExistUser(googleId):
        users_collection.update_one(
            {"id": googleId},
            { "$set": {"token" : token}}
        )
    else:
        users_collection.insert_one({'id': googleId, 'token': token})

def getUser(googleId):
    user = users_collection.find_one({'id': googleId})
    if user is None:
        return None
    return {'id':googleId, 'token': user['token']}

def isExistUser(googleId):
    if getUser(googleId):
        return True
    return False
def getDatetimeString(timestamp):
    date = datetime.fromtimestamp(timestamp).strftime('%d-%m-%y, %H:%M')
    return date


def getUserHistory(googleId):
    history = history_collection.find({'id': googleId})
    historyList = [d for d in history]
    # print([ d for d in history])
    result = [{'text': historyList[d]['text'], 'index':d,'time':  getDatetimeString(historyList[d]['time']), 'search_id': historyList[d]['search_id']} for d in range(len(historyList))]
    # times = [dict(d)['time'] for d in history]
    # [{'text': text, 'time':time} for text, time in [result,times]]
    return result
    # result = [{"text":Dict(d["text"],"index":i, "time": d["time"]}  for d, i in zip(history, range(len(list(history))+1))]
    # print(result)
    # return result

def isWatched(googleId, document):
    history = history_collection.find({'id': googleId, 'text':document})
    return history != None

from datetime import datetime

def addUserHistory(googleId, document, search_id):
    # if isWatched(googleId, document):
    #     history_collection.delete_one({'id': googleId, 'text': document})
    history_collection.insert_one({'id': googleId, 'text': document, 'time': datetime.now().timestamp(), 'search_id': search_id})
    

# addUserHistory("123", "heyyyophir", '951debec-d1da-11ec-836e-d07e35c972db')
# print(getUserHistory("123"))
# from google.oauth2 import id_token
# from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...
# def verifyToken(googleId, token):
#     try:
#         # Specify the CLIENT_ID of the app that accesses the backend:
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), '787276663684-065822sghlfajpjuo5ofd8ethbu35cc0.apps.googleusercontent.com')

#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')

#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')

#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         userid = idinfo['sub']
#     except ValueError:
#         # Invalid token
#         pass




