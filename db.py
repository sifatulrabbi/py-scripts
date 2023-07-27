import os
import stripe
from dotenv import load_dotenv
from pymongo import MongoClient
from pprint import pprint


def connect_to_db():
    mongo_url = os.getenv("MONGODB_URI", "")
    client = MongoClient(mongo_url)
    database_name = client.get_database().name
    print(f"connected db collection name: {database_name}")
    conn = client[database_name]
    return conn


if __name__ == "__main__":
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_LIVE_API_KEY")

    conn = connect_to_db()
    collections = {
        "users": conn.get_collection("users"),
        "accounts": conn.get_collection("accounts"),
        "appsumosubscriptions": conn.get_collection("appsumosubscriptions"),
    }

    user = collections["users"].find_one({"email": "sifatuli.r@gmail.com"})
    # pprint("\n---------- USER -------------")
    # pprint(user)

    if user["sumoling"]:
        sub = collections["appsumosubscriptions"].find_one(
            {"activation_email": user["email"]}
        )
        # pprint("\n---------- APPSUMO SUB -------------")
        # pprint(sub)

        if sub and ("togai_synced" not in sub or sub["togai_synced"] != True):
            account = collections["accounts"].find_one(
                {"_id": user["ownedAccount"]}
            )
            stripe_cus = stripe.Customer.retrieve(account["customer_id"])
            pprint(stripe_cus.to_dict()["metadata"])
