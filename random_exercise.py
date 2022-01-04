from requests import post
from lightdb import LightDB
from crontab import CronTab
from random import randrange, choice
import sys
import getpass

'''Needs crontab job like so: @daily cd /home/pi/shoorbapi/ && /usr/bin/python3 /home/pi/shoorbapi/random_exercise.py sched > /dev/null 2>&1'''

'''
Example db file:

{
    "google_exercise_image" : "google file id",
    "ifttt_exercise_event" : "random_exercise",
    "ifttt_key" : "key",
    "exercises" : [
        "Pushups",
        "Pistol Squats",
        "Handstand",
        "Quad Stretch",
        "Glute Stretch",
        "Ankle Mobility",
        "Roll-out Lats",
        "Plank",
        "Reverse Plank",
        "Sliding Disc Pushups",
        "Hollow Body",
        "Pull-ups",
        "Half Wheel",
        "Calf Raises",
        "Chest Stretch",
        "Pike Pushups"
    ]
}
'''

# number of exercises to generate for the day
NUM_TIMES = 3

# remove the existing jobs
def rem_jobs():
    user = getpass.getuser()
    cron = CronTab(user=user)
    for job in cron:
        if 'exercise' in job.comment:
            cron.remove(job)
            cron.write()

# schedule jobs
def sched_jobs():
    user = getpass.getuser()
    cron = CronTab(user=user)
    # get a random hour and minute between 10:00AM and 8:59PM
    for _ in range(NUM_TIMES):
        job = cron.new(command=f'cd /home/pi/shoorbapi/ && /usr/bin/python3 /home/pi/shoorbapi/random_exercise.py push > /dev/null 2>&1 # exercise')
        min = randrange(60)
        hour = randrange(10, 21)
        job.hour.on(hour)
        job.minute.on(min)
        cron.write()

# choose a random workout and push it to the fphone
def push_to_phone():
    db = LightDB("keys.json")
    ifttt_event = db.get("ifttt_exercise_event") # get the event
    # image is hosted on google drive use the URL fomrat below to display it
    google_image_id = db.get("google_exercise_image") # get the Google Drive image ID
    ifttt_key = db.get("ifttt_key") # get the key
    exercises = db.get("exercises")

    data = {
        "message_title" : "Exercise Time!",
        "message" : choice(exercises), # choose a random exercise from db
        "image_url" : f"https://drive.google.com/uc?id={google_image_id}"
    }

    # push notifcation to IFTTT app on mobile
    post(f'https://maker.ifttt.com/trigger/{ifttt_event}/json/with/key/{ifttt_key}', data=data)


# when run as main check the arguments and either schedule or push
if __name__ == '__main__':
    if sys.argv[1] == 'sched':
        rem_jobs()
        sched_jobs()
    if sys.argv[1] == 'push':
        push_to_phone()

