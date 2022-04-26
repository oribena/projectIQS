import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
# mongo_key = os.environ.get("mongo_key")
connection_string = os.environ.get("connection_string")

def getMongoClient():
    return MongoClient(connection_string)

mongo_client = getMongoClient()
db = mongo_client.Users
users_collection = db['UsersDetails']

def removeUsersCollection():
    users_collection.delete_many({})
# removeUsersCollection()


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




