import os
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CursorNotFound


def connect_to_db():
    try:
        client = MongoClient(
            os.getenv("MONGODB_PROD_URI"), serverSelectionTimeoutMS=5000
        )
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        print("Connected to the MongoDB database")
        return client
    except ConnectionFailure as cf:
        print("Error while connecting to the MongoDB database", cf)


client = connect_to_db()
db = client["helloscribe"]
Users = db["users"]
Accounts = db["accounts"]
AppSumoSubs = db["appsumosubscriptions"]


def get_info_from_db():
    try:
        doc = Users.find_one({"email": "christinebklyn1@yahoo.com"})
        pprint(doc)
    except CursorNotFound as err:
        print(err)
