import requests
import subprocess
import pandas as pd
import time

# user will:
# need to download Stellarium and set the default projection mode to 'equal area'
# need to set the screenshot location in Stellarium to "Screenshots" folder within the HLT project


def change_settings(url_main):
    """
    this function changes the Stellarium settings to get the correct screenshot setup, takes a screenshot, and
    saves that image to a specific folder within the HLT project
    """
    # take stellarium out of full screen mode
    """full_screen = requests.post(url_main + 'stelaction/do', data={'id': 'actionSet_Full_Screen_Global'})
    print("Fullscreen: ", full_screen)"""

    # show azimuthal grid
    azimuth_grid = requests.post(url_main + 'stelaction/do', data={'id': 'actionShow_Azimuthal_Grid'})
    #print("Azimuth: ", azimuth_grid)

    # remove atmosphere view
    atmosphere = requests.post(url_main + 'stelaction/do', data={'id': 'actionShow_Atmosphere'})
    #print("Atmosphere: ", atmosphere)

    # calculate julian day according to Stellarium reference
    date = pd.to_datetime("today") + pd.Timedelta(hours=6)
    ts = pd.Timestamp(date)
    julian = ts.to_julian_date()

    # set the date and time
    set_date_time = {'time': julian, 'timerate': 0, }
    time = requests.post(url_main + "main/time", data=set_date_time)
    #print("Time: ", time)

    # set location
    set_location = {'latitude': 30.6280, 'longitude': -96.3344, 'altitude': 0}
    location = requests.post(url_main + "location/setlocationfields", data=set_location)
    #print("Location: ", location)

    # set the sky view direction
    # [south, east, altitude]
    set_view = {'altAz': '[0.00001, 0, 1]'}
    view = requests.post(url_main + "main/view", data=set_view)
    #print("View: ", view)

    # set the sky view zoom level
    set_fov = {'fov': '190'}
    fov = requests.post(url_main + "main/fov", data=set_fov)
    #print("FOC: ", fov)


def take_screenshot(url_main):
    # create a screenshot of the current view
    screenshot = requests.post(url_main + 'stelaction/do', data={'id': 'actionSave_Screenshot_Global'})
    #print("Screenshot: ", screenshot)


def crop_selection_image():
    image_path = 'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\GUI Stellarium Photos'


def open_close_stellarium():
    # enable remote control plugin for Stellarium
    # open Stellarium before running this program
    url = "http://localhost:8090/api/"

    path = 'C:\\Program Files\\Stellarium\\stellarium.exe'
    proc_stellarium = subprocess.Popen(path)
    time.sleep(10)
    change_settings(url)
    time.sleep(3)
    take_screenshot(url)

    # Get a list of available action IDs:
    '''url_actions = "stelaction/list"
    actions = requests.get(url + url_actions)
    print(actions.status_code)
    if actions.status_code == 200:
        print(actions.json())
    
    url_properties = "stelproperty/list"
    properties = requests.get(url + url_properties)
    print(properties.status_code)
    if properties.status_code == 200:
        print(properties.json())'''

    proc_stellarium.kill()


# open_close_stellarium()
