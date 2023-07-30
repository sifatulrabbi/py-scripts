import stripe
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# stripe.api_key = os.getenv("XBOOKER_STRIPE_TEST_KEY")
stripe.api_key = os.getenv("STRIPE_LIVE_API_KEY")

# subs = stripe.Customer.create(
#     name="sifatul-test-3",
#     email="mdsifatulislam.rabbi@gmail.com",
#     metadata={"attachDefaultPricePlan": "false"},
# )
# pprint(subs)

cus = stripe.Customer.retrieve(id="cus_OJzlf2II6A5fWi")
pprint(cus)
