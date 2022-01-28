import requests
import json
import sys
import math
from datetime import datetime
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    # get the athan timings for the day
    lat = "47.619060"
    lon = "-122.337420"
    method = "2"  # isna
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method={method}"
    athan_times = requests.get(url).json()["data"]["timings"]

    prayers = [
        "Fajr",
        "Dhuhr",
        "Asr",
        "Maghrib",
        "Isha",
        #'Imsak',
        #'Sunrise',
        #'Midnight,
        # All the above is available via the API
        # if you add or remove please update the crontab file as well
    ]

    athan_times = {key: athan_times[key] for key in prayers}

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    for prayer in prayers:
        if athan_times[prayer] > current_time:
            next_athan = prayer
            break

    if current_time > athan_times["Isha"]:
        next_athan = "Fajr"

    next_time = athan_times[next_athan]

    time_1 = datetime.strptime(current_time, "%H:%M")
    time_2 = datetime.strptime(next_time, "%H:%M")
    remaining_time = time_2 - time_1
    remaining_time = remaining_time.total_seconds()
    remaining_time = remaining_time / 60
    if remaining_time >= 60:
        remaining_time = remaining_time / 60
        remaining_mins = remaining_time % 1 * 60
        remaining_mins = round(remaining_mins)
        remaining_hours = math.floor(remaining_time)
        remaining_hours = str(int(remaining_hours))
        remaining_mins = str(int(remaining_mins))
        remaining_time = f"{remaining_hours} hours and {remaining_mins} minutes"
    else:
        remaining_time = str(int(remaining_time))
        remaining_time = f"{remaining_time} minutes"

    host = "localhost"  # localhost
    token = "some key"
    domain = "tts"
    service = "google_translate_say"
    entity_id = "media_player.studio_display"

    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }

    url = f"http://{host}:8123/api/services/{domain}/{service}"
    data = {
        "entity_id": entity_id,
        "message": f"{remaining_time} remain until the next prayer call",
    }

    # play the message
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return "Prayer Times :)"
