import json


with open('config.json', 'r') as config_file:
    data = config_file.read()
config = json.loads(data)