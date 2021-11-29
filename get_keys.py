import json

def get_keys():
    with open("keys.json") as f:
        return json.load(f)