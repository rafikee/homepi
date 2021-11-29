import os
from google.cloud import storage
from random import randrange

# this bucket has the sounds that we'll randomly change
bucket_name = 'takbir'
file_to_play = 'play.mp3' # the name of the file that is currently playing
# All the buckets that we want to change
buckets = [
    'takbir',
    'fajr-athan',
    'full-athan'
]

#Environment variable for google authentication set in bashrc
#connect to the bucket
storage_client = storage.Client()

# loop through all the buckets and setup the new athan randomly
for bucket_name in buckets:

    bucket = storage_client.bucket(bucket_name)
    # remove the current playing file
    # try in case the file isn't there we don't care
    try:
        blob_old = bucket.blob(file_to_play)
        blob_old.delete()
    except:
        pass

    # get a list of all the file names in the bucket
    blobs = []
    for blob in storage_client.list_blobs(bucket_name):
        blobs.append(blob.name)

    # use the number of files to pick one at random
    count = len(blobs)
    new_file = blobs[randrange(0,count)]

    # setup the new file to play
    blob_new = bucket.blob(new_file)
    bucket.copy_blob(blob_new, bucket, file_to_play)