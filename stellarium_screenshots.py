import requests
import subprocess
import datetime
import jdcal as j
import pandas as pd
# open Stellarium before running this program

url_main = "http://localhost:8090/api/"

response = requests.get(url_main + "main/status")
print("Status: ", response.status_code)

# calculate julian day according to Stellarium reference
date = pd.to_datetime("today") + pd.Timedelta(hours=5)
ts = pd.Timestamp(date)
julian = ts.to_julian_date()

# set the date and time
set_date_time = {'time': julian, 'timerate': 0, }
time = requests.post(url_main + "main/time", data=set_date_time)
print("Time: ", time)

# set location
set_location = {'latitude': 30.6280, 'longitude': -96.3344, 'name': 'College Station', 'planet': 'Earth',
                'region': 'Northern America', 'role': 'X', 'state': 'Texas'}

# set the sky view direction
# [south, east, altitude]
set_view = {'altAz': '[0.001, 0, 1]'}
view = requests.post(url_main + "main/view", data=set_view)
print("View: ", view)

# set the sky view zoom level
set_fov = {'fov': '190'}
fov = requests.post(url_main + "main/fov", data=set_fov)
print("FOC: ", fov)

if response.status_code == 200:
    print("Time: ", response.json().get('time'))
    print("Location: ", response.json().get('location'))
    print("View: ", response.json().get('view'))
