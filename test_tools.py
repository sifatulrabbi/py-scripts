import stripe
import os
import requests
import json
from time import sleep
from dotenv import load_dotenv
from pprint import pprint
from tool_category_list import categories

load_dotenv()
stripe.api_key = os.getenv("STRIPE_LIVE_API_KEY")


def get_backend_url(path: str):
    return "http://localhost:3001/api" + path


def get_data(type: str):
    data = {
        "type": type,
        "tones": "",
        "target_lang": "EN-US",
        "description": "give me a content strategy for a spring water brand",
        "descriptionHTML": "<p>give me a content strategy for a spring water brand</p>",
        "source_lang": "EN-US",
        "journalistName": "",
        "domains": "",
        "company": "",
        "name": "",
        "role": "",
    }
    return json.dumps(data)


infected_arr = {}

try:
    for category in categories:
        print("----------------------------------")
        print(f"using -> {category['path']}")
        sleep(2)
        for tool in category["tools"]:
            print(f"testing -> {tool}")
            try:
                path = category["path"]
                response = requests.post(
                    url=get_backend_url(path),
                    headers={
                        "Authorization": "Bearer " + os.getenv("AUTH0_TOKEN"),
                        "Content-Type": "application/json",
                    },
                    data=get_data(tool),
                )
                print(f"    {response.status_code} {response.reason}")
                try:
                    result = response.json()
                    contents = result["results"]
                    if len(contents) > 1:
                        uniques = []
                        for content in contents:
                            text = content["text"]
                            if text in uniques:
                                infected_arr.setdefault(path, []).append(tool)
                                print(f"    {tool} tool has duplicate contents")
                            else:
                                uniques.append(text)
                except requests.exceptions.JSONDecodeError as err:
                    print(f"    error: unable to parse json. {err.strerror}")
            except requests.exceptions.HTTPError as err:
                print(f"    error: {tool} tool isn't working")
except:
    print("Loop closed unexpectedly")


with open("./tmp/tools-similar-contents.json", "w") as f:
    json.dump(infected_arr, f)
    f.close()

# try:
# customers = stripe.Customer.list(email="sifatuli.r@gmail.com")
# for cus in customers.list():
#     pprint(cus)
# except stripe.error.StripeError as err:
#     print(err)


# users: list[User] = []
# infected_users: list[User] = []

# with open(file="./tmp/sumolings.json") as f:
#     users = json.load(f)
#     f.close()

# for user in users:
#     try:
#         stripeCus = stripe.Customer.retrieve(
#             id=user["ownedAccount"]["customer_id"]
#         )
#         if stripeCus.get("deleted"):
#             infected_users.append(user)
#             print("Infected user found", user["email"])
#     except stripe.error.StripeError as err:
#         infected_users.append(user)
#         print("Infected user found", err)
#     except Exception as err:
#         print("An unexpected error occurred:", err)

# with open("./tmp/infected-users.json", "w") as f:
#     json.dump(infected_users, f)
#     f.close()

# """
# Take the infected users from the json file and create a short csv file
# """
# with open("./tmp/infected-users.json", "r") as f:
#     users = json.load(f)
#     f.close()
#     csvData = ["Email,Customer ID"]
#     for user in users:
#         csvData.append(
#             user["email"] + "," + user["ownedAccount"]["customer_id"]
#         )
#     with open("./tmp/infected-users.csv", "w") as f:
#         f.write("\n".join(csvData))
#         f.close()

# get_info_from_db()
