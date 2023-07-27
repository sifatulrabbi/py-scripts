import requests
import json

from os import getenv
from dotenv import load_dotenv
from pprint import pprint

from db import connect_to_db

if __name__ != "__main__":
    exit(0)

load_dotenv()

TOGAI_API_KEY = getenv("TOGAI_API_KEY")


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

"""
step 1: get the user info and accounts
"""
users = []
for email in user_emails:
    col = db.get_collection("users")
    user = col.find_one({"email": email})
    if not user["_id"]:
        print(f"User not found: {email}")
    else:
        account = db.get_collection("accounts").find_one(
            {"_id": user["ownedAccount"]}
        )
        if not account["_id"]:
            print(f"account not found for user: {email}")
        else:
            user["ownedAccount"] = account
            users.append(user)


"""
step 2: get their togai price plans
"""
full_user_info = []
for user in users:
    try:
        togai_plans = get_togai_pricing_schedules(
            user["ownedAccount"]["customer_id"]
        )
        # reduced_plans = []
        # for plan in togai_plans["data"]:
        #     reduced_plans.append(togai_plans["pricePlanId"])
        full_user_info.append(
            {
                "email": user["email"],
                "customer_id": user["ownedAccount"]["customer_id"],
                "sumoling": user["sumoling"],
                "togai_plans": togai_plans,
            }
        )
    except requests.exceptions.HTTPError as err:
        print(f"No togai plan found for: {user['email']}", err)


"""
step 3: if they are appsumo users get their appsumo subs
"""
for idx, user in enumerate(full_user_info):
    if not user["sumoling"]:
        continue
    appsumo_sub = db.get_collection("appsumosubscriptions").find_one(
        {"activation_email": user["email"]}
    )
    if appsumo_sub["_id"]:
        full_user_info[idx]["appsumo_plan"] = str(appsumo_sub["_id"])
        full_user_info[idx]["togai_synced"] = (
            appsumo_sub["togai_synced"]
            if "togai_synced" in appsumo_sub
            else False
        )


with open("tmp/tested_user_results.json", "w") as f:
    json.dump(full_user_info, f)
    f.close()
