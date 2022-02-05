# coding=utf-8
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import pandas as pd
from PIL import ImageTk
import ctypes
import Route_Demo


def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    OUTPUT_PATH_two = Path(__file__).parent
    ASSETS_PATH_two = OUTPUT_PATH_two / Path("./two_dim_area_buttons")
    return ASSETS_PATH_two / Path(path)


def get_coordinates(event):
    """
    this function gets the coordinates from mouse clicks within the skymap image
    """
    if len(coordinates_list) >= 4:
        coordinates_list.clear()

    coordinates_list.append([event.x-275, -1 * (event.y-300)])

    if len(coordinates_list) <= 2:
        canvas.create_text(
            150.0,
            570.0,
            anchor="nw",
            text=coordinates_list,
            fill="#000000",
            font=("Courier New", 20 * -1)
        )
    print(coordinates_list)


def bind_mouse(two_sel_window):
    """
    this function binds the mouse - button 1 to the get_coordinates event
    """
    two_sel_window.bind('<Button-1>', get_coordinates)


def unbind_mouse(two_sel_window):
    """
    this function unbinds the mouse - button 1 from events and sends the coordinates
    to the route planning subsystem
    """
    two_sel_window.unbind('<Button-1>')
    del coordinates_list[2]

    print("mouse unbound")
    print(coordinates_list)

    route_list = Route_Demo.two_dim(250, coordinates_list[0], coordinates_list[1], 10)
    routedf = pd.DataFrame(route_list)
    routedf.to_csv('Z:\\Route Data\\Scanning_Route.csv', index=False)
    with open('Z:\\Route Data\\Scanning_Key.txt', 'w') as f:
        f.write('0')
    two_sel_window.destroy()


def main(og_window):

    # remove the select mode window
    og_window.destroy()

    # set GUI clarity
    ctypes.windll.shcore.SetProcessDpiAwareness(3)
    global coordinates_list
    global canvas

    coordinates_list = []

    # create the GUI window for this mode
    two_sel_window = Tk()
    two_sel_window.geometry("900x600")
    two_sel_window.configure(bg="#A5A5A5")

    canvas = Canvas(
        two_sel_window,
        bg = "#A5A5A5",
        height = 600,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"), master=two_sel_window)
    button_1 = Button(
        two_sel_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: bind_mouse(two_sel_window)
    )
    button_1.place(
        x=585.0,
        y=430.0,
        width=258.0,
        height=61.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"), master=two_sel_window)
    button_2 = Button(
        two_sel_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command= lambda: unbind_mouse(two_sel_window),
        relief="flat"
    )
    button_2.place(
        x=585.0,
        y=489.0,
        width=258.0,
        height=61.0
    )

    canvas.create_text(
        606.0,
        49.0,
        anchor="nw",
        text="2-D Area Selection",
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
        text="will scan a rectangular area",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        128.0,
        anchor="nw",
        text="of the skymap.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        160.0,
        anchor="nw",
        text="Click the ‘Select Corners’",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        180.0,
        anchor="nw",
        text="button. Selecting this",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        200.0,
        anchor="nw",
        text="button will prompt the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        220.0,
        anchor="nw",
        text="program to record the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        240.0,
        anchor="nw",
        text="coordinates of the next two",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        260.0,
        anchor="nw",
        text="mouse clicks within the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        280.0,
        anchor="nw",
        text="image.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        312.0,
        anchor="nw",
        text="Select a lower left corner",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        332.0,
        anchor="nw",
        text="first and then an upper",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        352.0,
        anchor="nw",
        text="right corner.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        383.0,
        anchor="nw",
        text="Then, select ‘Initiate",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        403.0,
        anchor="nw",
        text="Scan’.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png"
    img = ImageTk.PhotoImage(file=path, master=two_sel_window)
    canvas.create_image(275, 300, image=img)

    two_sel_window.resizable(False, False)
    two_sel_window.mainloop()
