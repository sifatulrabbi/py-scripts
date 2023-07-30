import requests
from pprint import pprint

url = "http://localhost:8000/storage/v1/buckets/creation-test"

auth_token = ""
with open("tmp/firebase_auth_token.txt", "r") as f:
    auth_token = f.read()
    f.close()

try:
    res = requests.post(
        url=url,
        headers={"authorization": auth_token},
        params={"organizationId": "sifatul-test-org-1"},
    )
    try:
        data = res.json()
        pprint(data)
    except requests.exceptions.JSONDecodeError as err:
        pprint(err)
except requests.exceptions.HTTPError as err:
    pprint(err)

# base_url = "http://localhost:8000/storage/v1"
# user_id = "ufpY09WJ8oY4oht6lEhCYzKoFOF2"
# # /buckets/files?organizationId=sifatuls-org&source=org


# def get_url(path: str):
#     return base_url + path


# def get_auth_token():
#     token = ""
#     with open("tmp/firebase_auth_token.txt", "r") as f:
#         token = f.read()
#         f.close()
#     return token


# def get_all_files():
#     try:
#         token = get_auth_token()
#         res = requests.get(
#             url=get_url("/buckets/files"),
#             params={"organizationId": "sifatuls-org", "source": "org"},
#             headers={
#                 "authorization": f"Bearer {token}",
#                 "user-id": user_id,
#             },
#         )
#         try:
#             return res.json()
#         except requests.exceptions.JSONDecodeError as err:
#             print(err)
#             return None
#     except requests.exceptions.HTTPError as err:
#         print(err)
#         return None


# if __name__ == "__main__":
#     data = get_all_files()
#     pprint(data["data"]["storageInfo"]) if "data" in data else pprint(data)
