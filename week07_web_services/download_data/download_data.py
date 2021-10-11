"""
    Run this file with the command:

        poetry run python download_data.py

"""

import datetime
import json
import requests

print('Downloading the Indego stations data...')
response = requests.get("https://www.rideindego.com/stations/json/")
data = response.json()

print('Saving the data to disk...')
now = datetime.datetime.now()
with open(f'indego_station_status_{now}.geojson', 'w') as outfile:
    json.dump(data, outfile)

print('Done.')
