import requests
import json
import sys
from get_keys import get_keys # get the function that reads keys from json

keys = get_keys() # read in all the keys
token = keys['shoorbapi_token'] # HASS API token
entity_id = keys['entity_id'] # speaker ID or speaker group ID

host = 'localhost'
domain = 'media_player'
service = 'volume_set'
entity_id = entity_id
token = token

url = f"http://{host}:8123/api/services/{domain}/{service}"
headers = {
    "Authorization": f"Bearer {token}",
    "content-type": "application/json",
}

athan_option = sys.argv[1]

# lower the volume if Fajr
volume = .4 if athan_option == 'fajr' else .5

if athan_option == 'fajr':
    media = 'https://storage.googleapis.com/fajr-athan/play.mp3'
elif athan_option == 'full':
    media = 'https://storage.googleapis.com/full-athan/play.mp3'
else:
    media = 'https://storage.googleapis.com/takbir/play.mp3'


data = {
    'entity_id' : entity_id,
    'volume_level' : volume
}

# set the volume
r = requests.post(url, headers=headers, data=json.dumps(data))

service = 'play_media'
url = f"http://{host}:8123/api/services/{domain}/{service}"
data = {
    'entity_id' : entity_id,
    'media_content_type' : 'audio/mp3',
    'media_content_id' : media,
}
# play the media
r = requests.post(url, headers=headers, data=json.dumps(data))