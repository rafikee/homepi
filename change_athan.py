import os
from random import randrange
import shutil

file_to_play = 'play.mp3' # the name of the file that is currently playing
# All the buckets that we want to change
buckets = [
    'takbir',
    'fajr',
    'full'
]

# loop through all the buckets and setup the new athan randomly
for bucket in buckets:
    # remove the current playing file
    # try in case the file isn't there we don't care
    try:
        os.remove(f"static/{bucket}/{file_to_play}")
    except:
        pass
    files = os.listdir(f"static/{bucket}")
    files = [x for x in files if '.git' not in x] # drop these

    # use the number of files to pick one at random
    count = len(files)
    new_file = files[randrange(0,count)]

    # setup the new file to play
    shutil.copy(f'static/{bucket}/{new_file}', f'static/{bucket}/{file_to_play}')