"This is the old version that runs direclty on the pi not using GCP"

"This should be scheduled to run in crontab at set times per day"
"""0 7-22 * * * cd /home/pi/shoorbathan/ && /usr/bin/python3 /home/pi/shoorbathan/get_crypto.py > /dev/null 2>&1"""

from requests import get, post
from lightdb import LightDB

"""
db file example

{
    "ifttt_crypto_event" : "event_name",
    "ifttt_key" : "key",
    "google_crypto_image" : "google file id",
    "crypto" : ["dogecoin", "ripple", "decentraland", "shiba-inu" ,"helium", "basic-attention-token", "micropets"]
}
"""

# get db from json file with keys
db = LightDB("keys.json")
ifttt_event = db.get("ifttt_crypto_event")  # get the event
google_image_id = db.get("google_crypto_image")  # get the Google Drive image ID
ifttt_key = db.get("ifttt_key")  # get the key

prices = []
s = ""  # string to hold all the values we'll push to IFTTT

coins = db.get("crypto")
for coin in coins:
    x = get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"
    ).json()[0]
    price = round(float(x["current_price"]), 2)
    if price == 0:
        price = round(
            float(x["current_price"]) * 1000, 2
        )  # if the price is super low multiply it so we can see it scale
        if price == 0:
            price = round(
                float(x["current_price"]) * 100000, 2
            )  # if the price is still super low
    prices.append(f"{x['symbol']}: {price}")
value = " | ".join(
    prices
)  # create one big string for all the prices that we'll use to pipe into the variable to IFTTT

data = {
    "message_title": "Crypto Update",
    "message": value,
    "image_url": f"https://drive.google.com/uc?id={google_image_id}",
}

# push prices to IFTTT notification on phone
post(
    f"https://maker.ifttt.com/trigger/{ifttt_event}/json/with/key/{ifttt_key}",
    data=data,
)
