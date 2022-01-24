"""
How to deploy:
    - Create an IFTTT worflow
        - if this = webhook with a json payload
            - name the event 'crypto_script'
        - then that = notification
            - choose the rich one
            - the title and message are irrelavant as they will overwrriten
        - add a filter code step in between the two:
            let payload = JSON.parse(MakerWebhooks.jsonEvent.JsonPayload)
            IfNotifications.sendRichNotification.setTitle(payload.message_title)
            IfNotifications.sendRichNotification.setMessage(payload.message)
            IfNotifications.sendRichNotification.setImageUrl(payload.image_url)
        - locate the api key for IFTTT under your account
            - go to My services
            - then choose Webhooks and go to settings
    - Create a Google Cloud Project that can do billing
    - Enable the following APIs in the project
        - Google Sheets
        - Google Drive
        - Secrets Manager
        - Cloud Functions
    - Add the following secrets in the secrets manager
        - 'ifttt_api_key' as a string
        - url for image to be used in notification
            - call it 'crypto_image_url'
        - default app engine service account json key as a file
            - call it 'service_account_json'
            - this can be downloaded from IAM
            - other service account can be created an used
            - if so make sure to grant this account permission to the funcion
    - In the IAM console add a new role to give the service account access to secret manager secret accessor
    - Create a google sheet with one column titled "coins"
        - name the sheet 'get crypto'
        - share this sheet with the service account you are using
        - use their service account email address
        - add in row by row the names of the coins of interest

Use the following command to deploy:
* change the project_id accordingly
"""
# gcloud functions deploy get_crypto --set-env-vars project_id=home-automation-272816 --runtime python39 --trigger-http --allow-unauthenticated
from requests import get, post
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import secretmanager
import os
import json

PROJECT_ID = os.environ["project_id"]
SHEET_NAME = "get crypto"
IFTTT_EVENT = "crypto_script"


def get_secret(secret_name: str):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    secret = response.payload.data.decode("UTF-8")
    try:
        secret = json.loads(secret)
    except:
        pass
    return secret  # returns a json or a string depending on the secret type


def get_crypto(request):
    ifttt_key = get_secret("ifttt_api_key")
    service_account_json = get_secret("service_account_json")
    crypto_image_url = get_secret("crypto_image_url")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        service_account_json, scope
    )

    client = gspread.authorize(creds)
    data = client.open(SHEET_NAME).sheet1.get_all_records()
    coins = [x["coins"] for x in data if "coins" in x]

    prices = []
    s = ""  # string to hold all the values we'll push to IFTTT

    error_coins = []
    error = False

    if not coins:
        value = "The Google Sheet is missing the 'coins' column"

    for coin in coins:
        x = get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"
        ).json()
        if not x:
            error = True
            error_coins.append(coin)
            continue
        x = x[0]
        price = x.get("current_price", None)
        symbol = x.get("symbol", None)
        if not price or not symbol:
            error = True
            error_coins.append(coin)
            continue
        price = round(float(price), 2)
        if price == 0:
            price = round(
                float(price) * 1000, 2
            )  # if the price is super low multiply it so we can see it scale
            if price == 0:
                price = round(
                    float(price) * 100000, 2
                )  # if the price is still super low
        prices.append(f"{symbol}: {price}")

    if prices:
        value = " | ".join(
            prices
        )  # create one big string for all the prices that we'll use to pipe into the variable to IFTTT
        if error:
            value += ". FYI these coins failed: "
            value += ", ".join(error_coins)

    if not value:
        value = "Error in getting crypto. Make sure all the names are valid."

    data = {
        "message_title": "Crypto Update",
        "message": value,
        "image_url": crypto_image_url,
    }

    # push prices to IFTTT notification on phone
    post(
        f"https://maker.ifttt.com/trigger/{IFTTT_EVENT}/json/with/key/{ifttt_key}",
        data=data,
    )
    return "Yay Crypto!"
