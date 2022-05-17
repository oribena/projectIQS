import os
from dotenv import load_dotenv
from numpy import true_divide
import pymongo
from pymongo import MongoClient
from cryptography.fernet import Fernet

load_dotenv()
# mongo_key = os.environ.get("mongo_key")
connection_string = os.environ.get("connection_string")

def getMongoClient():
    return MongoClient(connection_string)

mongo_client = getMongoClient()
db = mongo_client.Users
users_collection = db['UsersDetails']
fernet = Fernet(b'Txrr9K3_rAkjMCtvzk4c96eF5lamUuDlSB6omyOJrKU=')

def generate_key():
    return Fernet.generate_key()

def removeUsersCollection():
    users_collection.delete_many({})
# removeUsersCollection()

def addUser(user_name, email, password):
    if not isExistUser(email):
        encMessage = fernet.encrypt(password.encode())
        users_collection.insert_one({'userName':user_name, 'email': email, 'password': encMessage})
        return True
    else:
        return False

def getUser(email):
    user = users_collection.find_one({'email': email})
    if user is None:
        return None
    password = fernet.decrypt(user['password']).decode()
    return {'userName':user['userName'], 'email':email, 'password': password}

def isExistUser(email):
    if getUser(email):
        return True
    return False




addUser("ophir","ophir@gmail.com", "ophiriiiii")
addUser("ori","ori@gmail.com", "ophiriiiii")
# getUser("ophir@gmail.com")
# addUser("ophir","ophir@gmail.com", "ophiriiiii")
    



