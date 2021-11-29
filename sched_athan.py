from crontab import CronTab
from get_keys import get_keys
from prayertimes import PrayTimes
import time
import os

# get all the variables from our json file
keys = get_keys()
lat = keys['lat']
lon = keys['lon']

# get the path where all the files are
path = os.getenv('shoorbapi_path')

dt = time.localtime()
tz = int(time.timezone / -3600) # get the timezone offset in hours non-DST
PT = PrayTimes('ISNA') # set the calc method
athan_times = PT.getTimes((dt.tm_year, dt.tm_mon, dt.tm_mday),(lat, lon), tz, dt.tm_isdst) # get the times

prayers = [
    'fajr',
    'dhuhr',
    'asr',
    'maghrib',
    'isha',
    #'imsak',
    #'sunrise',
    #'midnight,
    # All the above is available via the API
    # if you add or remove please update the crontab file as well
]

athan_times = {key: athan_times[key] for key in prayers}

# convert the time the API gives us to hours and minutes to use with cron
athan_cron = {}
for prayer in athan_times:
    athan_cron[prayer] = {'hour' : int(athan_times[prayer].split(':')[0]), 'min' : int(athan_times[prayer].split(':')[1])}

# schedule all the cron jobs
cron = CronTab(user='pi')
for job in cron:
    if 'athan' in job.comment:
        cron.remove(job)
        cron.write()
for prayer, timing in athan_cron.items():
    # set the parameter that gets passed to the athan script
    if prayer == 'fajr':
        athan = 'fajr' # Play the fajr file
    elif prayer == 'maghrib':
        athan = 'full' # play the full athan
    else:
        athan = 'takbir' # play only takbir
    
    # recreate all the jobs again
    job = cron.new(command=f'{path}/play_athan.sh {athan} > /dev/null 2>&1 # athan_{prayer}')
    job.hour.on(timing['hour'])
    job.minute.on(timing['min'])
    cron.write()