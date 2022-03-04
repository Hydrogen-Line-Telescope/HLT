# coding=utf-8
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, END, Label
import pandas as pd
from PIL import ImageTk
import ctypes
import glob
import time
import Route_Demo
import stellarium_screenshots
import image_processing
import image_overlay
import GUI_display_results


def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    OUTPUT_PATH_one_sweep = Path(__file__).parent
    ASSETS_PATH_one_sweep = OUTPUT_PATH_one_sweep / Path("./two_dim_sweep_buttons")
    return ASSETS_PATH_one_sweep / Path(path)


def coord_text():
    coord_text.var = Label(canvas,
                           text=str(coordinates_list[0]),
                           fg="#000000",
                           bg="#A5A5A5",
                           font=("Courier New", 20 * -1))
    coord_text.var.place(x=220, y=570)


def get_coordinates(event):
    """
    this function gets the coordinates from mouse clicks within the skymap image
    """
    '''if len(coordinates_list) >= 2:
        coordinates_list.clear()'''

    coordinates_list.append([event.x - 275, -1 * (event.y - 300)])

    print(coordinates_list)
    if len(coordinates_list) == 1:
        coord_text()
    elif len(coordinates_list) >= 2:
        coord_text.var["text"] = "Click R"


def bind_mouse(one_sweep_window):
    """
    this function binds the mouse - button 1 to the get_coordinates event
    """
    one_sweep_window.bind('<Button-1>', get_coordinates)


def unbind_mouse(one_sweep_window, entry_1):
    """
    this function unbinds the mouse - button 1 from events and sends the coordinates
    to the route planning subsystem
    """
    one_sweep_window.unbind('<Button-1>')
    del coordinates_list[1]

    print("mouse unbound")
    print(coordinates_list)

    hr_duration = int(entry_1.get())
    min_duration = hr_duration * 60
    num_scans = (min_duration / 15) + 1

    route_list = Route_Demo.one_terra(250, coordinates_list[0])
    routedf = pd.DataFrame(route_list)
    routedf = routedf.transpose()

    routedf.to_csv('Z:\\Route Data\\Scanning_Route.csv', index=False)
    with open('Z:\\Route Data\\Route_Key.txt', 'w') as f:
        f.write('0')
    one_sweep_window.destroy()

    image_gui_integration(hr_duration, num_scans)


def image_gui_integration(hr_duration, num_scans):
    """
    this function integrates the image processing and GUI subsystems
    """

    num_scans = int(num_scans)
    # call the time tracker function to start taking Stellarium screenshots
    time_list = stellarium_screenshots.time_tracker(hr_duration)

    # after the images are taken and cropped
    while True:
        with open('Z:\\Signal Data\\Signal_Key.txt') as c:
            write_check = c.readlines()

        print(write_check)
        if write_check[0] == '1':
            break
        else:
            print("sleepy_scan")
            time.sleep(10)

    # continue with image processing
    # read frequency and magnitude data into pandas dataframes
    freqdf = pd.read_csv('Z:\\Signal Data\\freq_data.csv')
    magdf = pd.read_csv('Z:\\Signal Data\\mag_data.csv')

    # call the heatmap function with the data
    # assuming that the heatmap data is in columns from left - the first scan - to right - the last scan
    image_processing.one_dim_sweep_rpa(freqdf, magdf, num_scans)

    # get the size of the heatmap for image overlay
    heatmap_size = image_overlay.one_dim_terr_rpa_coordinates(coordinates_list)

    # get cropped stellarium image paths
    cropped_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped*')
    # make sure they are in numerical order
    cropped_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    # get heatmap image paths
    heatmap_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Heatmaps\\Heatmap*')
    # make sure they are in numerical order
    heatmap_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    # send files in order to the overlay function
    # save to the Overlays folder
    for i in range(0, num_scans):
        image_overlay.image_overlay(heatmap_files[i], cropped_files[i], heatmap_size, str(i))

    # create a gif
    # GUI_display_results.clear_folder('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results')
    # GUI_display_results.create_transparent_gif(time_list)
    GUI_display_results.main(num_scans, time_list)


def reset_selection(two_sel_window):
    two_sel_window.unbind('<Button-1>')
    coordinates_list.clear()
    coord_text.var["text"] = ""


def main(og_window):
    # remove the select mode window
    og_window.destroy()

    # set GUI clarity
    # ctypes.windll.shcore.SetProcessDpiAwareness(3)
    global coordinates_list
    global canvas

    coordinates_list = []

    # create the GUI window for this mode
    one_sweep_window = Tk()
    one_sweep_window.geometry("900x600")
    one_sweep_window.configure(bg="#A5A5A5")

    canvas = Canvas(
        one_sweep_window,
        bg="#A5A5A5",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        one_sweep_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: bind_mouse(one_sweep_window)
    )
    button_1.place(
        x=585.0,
        y=460.0,
        width=258.0,
        height=61.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"), master=one_sweep_window)
    button_2 = Button(
        one_sweep_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: unbind_mouse(one_sweep_window, entry_1),
        relief="flat"
    )
    button_2.place(
        x=585.0,
        y=519.0,
        width=258.0,
        height=61.0
    )

    reset_image = PhotoImage(
        file=relative_to_assets("reset_button.png"))
    reset_button = Button(
        image=reset_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: reset_selection(one_sweep_window),
        relief="flat"
    )
    reset_button.place(
        x=4.0,
        y=4.0,
        width=34.0,
        height=34.0
    )

    canvas.create_text(
        588.0,
        46.0,
        anchor="nw",
        text="1-D Terrestrial Sweep",
        fill="#000000",
        font=("Courier New", 20 * -1)
    )

    canvas.create_text(
        560.0,
        88.0,
        anchor="nw",
        text="In this mode the antenna",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        108.0,
        anchor="nw",
        text="will scan a point as the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        128.0,
        anchor="nw",
        text="earth rotates.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        153.0,
        anchor="nw",
        text="Enter a duration, 1-5hr.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        173.0,
        anchor="nw",
        text="Click the ‘Select Point’",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        193.0,
        anchor="nw",
        text="button. Selecting this",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        213.0,
        anchor="nw",
        text="button will prompt the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        233.0,
        anchor="nw",
        text="program to record the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        253.0,
        anchor="nw",
        text="coordinates of the next",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        273.0,
        anchor="nw",
        text="mouse click within the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        293.0,
        anchor="nw",
        text="image.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        319.0,
        anchor="nw",
        text="The antenna will rotate to",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        339.0,
        anchor="nw",
        text="the selected point and scan",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        359.0,
        anchor="nw",
        text="that area for the duration",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        379.0,
        anchor="nw",
        text="specified.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        714.0,
        431.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#9E83AB",
        highlightthickness=0,
    )
    entry_1.insert(END, '1')
    entry_1.place(
        x=602.0,
        y=408.0 + 18,
        width=224.0,
        height=28.0
    )

    canvas.create_text(
        597.0,
        409.0,
        anchor="nw",
        text="Duration (1-5hr)",
        fill="#FFFFFF",
        font=("Courier New", 18 * -1)
    )

    path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png"
    img = ImageTk.PhotoImage(file=path, master=one_sweep_window)
    canvas.create_image(275, 300, image=img)

    one_sweep_window.resizable(False, False)
    one_sweep_window.mainloop()
