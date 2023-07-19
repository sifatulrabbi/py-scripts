import stripe
import os
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()
stripe.api_key = os.getenv("STRIPE_LIVE_API_KEY")

try:
    customers = stripe.Customer.list(email="sifatuli.r@gmail.com")
    for cus in customers.list():
        pprint(cus)
except stripe.error.StripeError as err:
    print(err)


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
