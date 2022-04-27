import requests
import subprocess
import pandas as pd
import time
import os
import glob
from PIL import Image, ImageDraw
import numpy as np
from datetime import datetime

# user will:
# need to download Stellarium and set the default projection mode to 'equal area'
# need to set the screenshot location in Stellarium to "Screenshots" folder within the HLT project


def crop_image(im, num_image, mode):
    """
    this function takes the screenshot output by stellarium and crops the image to fit
    within the GUI as a lower quality circle
    """

    width, height = im.size  # Get dimensions

    if mode == "2D":
        # 30-35 ish degree circle for 2D terrestrial
        left = (width - 600) / 2
        top = (height - 600) / 2
        right = (width + 600) / 2
        bottom = (height + 600) / 2
    else:
        # 950 for a  55 degree circle, 1250 for an 85 degree circle
        left = (width - 950) / 2
        top = (height - 950) / 2
        right = (width + 950) / 2
        bottom = (height + 950) / 2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))

    img = im.convert("RGB")
    npImage = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png')

    im = Image.open(
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png')
    width, height = im.size  # Get dimensions
    # print(width, height)

    new_im = im.resize((500, 500), Image.ANTIALIAS)
    width, height = im.size  # Get dimensions
    # print(width, height)
    # cropped images labeled as cropped_stellarium-#.png
    new_im.save(
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png',
        'PNG',
        quality=100)


def clear_folder(folder_path):
    """
    this function clears all previous screenshots from the Screenshots folder
    """
    files = glob.glob(folder_path + '\\*')
    for f in files:
        os.remove(f)


def time_tracker(hr_duration, mode):
    """
     this function will take a new stellarium screenshot every 15 minutes for the two terrestrial scanning modes
    """
    time_list = []
    # first, clear the Screenshots folder to get rid of the screenshot taken for the GUI display
    clear_folder('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots')

    # take a screenshot every 15 min - every 3.75 degrees of earth rotation
    min_duration = hr_duration * 60
    num_screenshots = (min_duration / 15) + 1
    print(num_screenshots)

    url = "http://localhost:8090/api/"
    path = 'C:\\Program Files\\Stellarium\\stellarium.exe'
    proc_stellarium = subprocess.Popen(path)
    time.sleep(10)
    change_settings(url)
    time.sleep(5)

    # 15 min = 840 seconds
    # - 10 seconds of sleep for stellarium to open
    # time.sleep(830)

    # currently takes a screenshot every 10 seconds
    for i in range(0, int(num_screenshots)):
        print("screenshot:", i)
        # time.sleep(840)
        stellarium_current_time(url)
        take_screenshot(url)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_list.append(str(current_time))
        time.sleep(5)

    proc_stellarium.kill()
    print(time_list)

    # crop all of the stellarium screenshots for the image overlay function
    # get all stellarium screenshots from the folder
    files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\*')

    # make sure the list of files is in ascending order by the number of the screenshot
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for i in range(0, len(files)):
        print(files[i])
        image = Image.open(files[i])
        # pass the image and image number to the crop_image function
        crop_image(image, str(i), mode)

    return time_list


def stellarium_current_time(url_main):
    # calculate julian day according to Stellarium reference
    date = pd.to_datetime("today") + pd.Timedelta(hours=6)
    ts = pd.Timestamp(date)
    julian = ts.to_julian_date()

    # set the date and time
    set_date_time = {'time': julian, 'timerate': 0, }
    time = requests.post(url_main + "main/time", data=set_date_time)


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
    # print("Azimuth: ", azimuth_grid)

    # remove atmosphere view
    atmosphere = requests.post(url_main + 'stelaction/do', data={'id': 'actionShow_Atmosphere'})
    # print("Atmosphere: ", atmosphere)

    # calculate julian day according to Stellarium reference
    date = pd.to_datetime("today") + pd.Timedelta(hours=6)
    ts = pd.Timestamp(date)
    julian = ts.to_julian_date()

    # set the date and time
    set_date_time = {'time': julian, 'timerate': 0, }
    time = requests.post(url_main + "main/time", data=set_date_time)
    # print("Time: ", time)

    # set location
    set_location = {'latitude': 30.6280, 'longitude': -96.3344, 'altitude': 0}
    location = requests.post(url_main + "location/setlocationfields", data=set_location)
    # print("Location: ", location)

    # set the sky view direction
    # [south, east, altitude]
    set_view = {'altAz': '[0.00001, 0, 1]'}
    view = requests.post(url_main + "main/view", data=set_view)
    # print("View: ", view)

    # set the sky view zoom level
    set_fov = {'fov': '190'}
    fov = requests.post(url_main + "main/fov", data=set_fov)
    # print("FOC: ", fov)


def take_screenshot(url_main):
    # create a screenshot of the current view
    screenshot = requests.post(url_main + 'stelaction/do', data={'id': 'actionSave_Screenshot_Global'})
    # print("Screenshot: ", screenshot)


def crop_selection_image():
    image_path = 'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\GUI Stellarium Photos'


def open_close_stellarium():
    start_time = time.time()
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
    # print("program time in seconds", (time.time() - start_time))

# time_tracker(1)
