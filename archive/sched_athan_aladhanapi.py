"Archived version of the athan scheduler"

from crontab import CronTab
from requests import get
from get_keys import get_keys
import os

keys = get_keys()  # get lat and lon from json file
lat = keys["lat"]
lon = keys["lon"]
path = os.getenv("shoorbathan")

# Must already have a line in cron for each prayer like so:
"""* * * * * /home/pi/shoorbathan/play_athan.sh takbir >/dev/null 2>&1 # athan_Isha"""
# the prayer name in the comment must match the string in the list of prayer names below

# get the athan timings for the day
method = "2"  # isna
url = (
    f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method={method}"
)
athan_times = get(url).json()["data"]["timings"]

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

# convert the time the API gives us to hours and minutes to use with cron
athan_cron = {}
for prayer in athan_times:
    athan_cron[prayer] = {
        "hour": int(athan_times[prayer].split(":")[0]),
        "min": int(athan_times[prayer].split(":")[1]),
    }

# schedule all the cron jobs
cron = CronTab(user="pi")
for job in cron:
    if "athan" in job.comment:
        cron.remove(job)
        cron.write()
for prayer, timing in athan_cron.items():
    # set the parameter that gets passed to the athan script
    if prayer == "Fajr":
        athan = "fajr"  # Play the fajr file
    elif prayer == "Maghrib":
        athan = "full"  # play the full athan
    else:
        athan = "takbir"  # play only takbir

    # recreate all the jobs again
    job = cron.new(
        command=f"{path}/play_athan.sh {athan} > /dev/null 2>&1 # athan_{prayer}"
    )
    job.hour.on(timing["hour"])
    job.minute.on(timing["min"])
    cron.write()
