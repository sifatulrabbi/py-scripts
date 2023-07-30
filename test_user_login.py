import requests
import json
import stripe

from os import getenv
from dotenv import load_dotenv
from pprint import pprint

from db import connect_to_db

if __name__ != "__main__":
    exit(0)

load_dotenv()

TOGAI_API_KEY = getenv("TOGAI_API_KEY")
STRIPE_KEY = getenv("STRIPE_LIVE_API_KEY")
stripe.api_key = STRIPE_KEY


def get_togai_pricing_schedules(id: str) -> dict:
    url = f"https://api.togai.com/accounts/{id}/pricing_schedules"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOGAI_API_KEY}",
    }
    res = requests.get(url, headers=headers)
    return res.json()


db = connect_to_db()
user_emails = []
# load the users emails
with open("./assets/users_to_test.json", "r") as f:
    user_emails = json.load(f)
    f.close()

user_col = db.get_collection("users")
account_col = db.get_collection("accounts")
appsumosub_col = db.get_collection("appsumosubscriptions")

users_data = []

for email in user_emails:
    user = user_col.find_one({"email": email})
    appsumo_sub = appsumosub_col.find_one({"activation_email": email})
    if not user:
        print(f"not found -> {email}")
        if appsumo_sub and appsumo_sub["_id"]:
            print(f"{email} has appsumo sub: {appsumo_sub['_id']}")
    else:
        account = account_col.find_one({"_id": user["ownedAccount"]})
        stripe_cus = stripe.Customer.retrieve(account["customer_id"])
        users_data.append(
            {
                "email": email,
                "customer_id": stripe_cus.id,
                "metadata": stripe_cus.to_dict()["metadata"],
                "appsumo_sub": appsumo_sub["plan_id"]
                if appsumo_sub
                else "not-found",
                "togai_synced": appsumo_sub["togai_synced"]
                if appsumo_sub and "togai_synced" in appsumo_sub
                else "not-found",
            }
        )

with open("tmp/infected-users.json", "w") as f:
    json.dump(users_data, f)
    f.close()
