# coding=utf-8
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label
import pandas as pd
from PIL import ImageTk
import ctypes
import Route_Demo
import error_message_1

'''canvas = 0
coordinates_list = []
'''


def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    OUTPUT_PATH_two = Path(__file__).parent
    ASSETS_PATH_two = OUTPUT_PATH_two / Path("./two_dim_area_buttons")
    return ASSETS_PATH_two / Path(path)


def coord_text():
    coord_text.var = Label(canvas,
                           text=coordinates_list,
                           fg="#000000",
                           bg="#A5A5A5",
                           font=("Courier New", 20 * -1))
    coord_text.var.place(x=150, y=570)


def get_coordinates(event):
    """
    this function gets the coordinates from mouse clicks within the skymap image
    """
    if len(coordinates_list) >= 4:
        coordinates_list.clear()

    coordinates_list.append([event.x - 275, -1 * (event.y - 300)])

    print(coordinates_list)
    if len(coordinates_list) == 1:
        coord_text()
    elif len(coordinates_list) == 2:
        coord_text.var["text"] = ""
        coord_text()


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

    print("test", coordinates_list)

    two_sel_window.destroy()

    print("mouse unbound")
    print(coordinates_list)

    lower_left_coord = [0, 0]
    upper_right_coord = [0, 0]
    # lower left is smaller x, smaller y
    # upper right is larger x, larger y

    # compare x's
    if coordinates_list[0][0] < coordinates_list[1][0]:
        lower_left_coord[0] = coordinates_list[0][0]
        upper_right_coord[0] = coordinates_list[1][0]
    else:
        upper_right_coord[0] = coordinates_list[0][0]
        lower_left_coord[0] = coordinates_list[1][0]

    # compare y's
    if coordinates_list[0][1] < coordinates_list[1][1]:
        lower_left_coord[1] = coordinates_list[0][1]
        upper_right_coord[1] = coordinates_list[1][1]
    else:
        upper_right_coord[1] = coordinates_list[0][1]
        lower_left_coord[1] = coordinates_list[1][1]

    # print(lower_left_coord)
    # print(upper_right_coord)

    # check rectangle dimensions
    if upper_right_coord[0] - lower_left_coord[0] < 15:
        # print("Selected area is too small.")
        error_message_1.selection_size_error()
    elif upper_right_coord[1] - lower_left_coord[1] < 15:
        # print("Selected area is too small.")
        error_message_1.selection_size_error()
    else:
        route_list = Route_Demo.two_dim(250, lower_left_coord, upper_right_coord, 10)
        routedf = pd.DataFrame(route_list)
        # Z:\\Route Data\\Scanning_Route.csv
        # print("dataframe", routedf)
        routedf.to_csv('Route Data\\Scanning_Route.csv', index=False)

    '''with open('Z:\\Route Data\\Scanning_Key.txt', 'w') as f:
        f.write('0')'''


def reset_selection(two_sel_window):
    two_sel_window.unbind('<Button-1>')
    coordinates_list.clear()
    coord_text.var["text"] = ""


def main(og_window):
    # remove the select mode window
    og_window.destroy()

    # set GUI clarity
    ctypes.windll.shcore.SetProcessDpiAwareness(3)
    global coordinates_list
    global canvas

    coordinates_list = []
    coordinates_list.clear()

    print("test", coordinates_list)

    # create the GUI window for this mode
    two_sel_window = Tk()
    two_sel_window.geometry("900x600")
    two_sel_window.configure(bg="#A5A5A5")

    canvas = Canvas(
        two_sel_window,
        bg="#A5A5A5",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
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
        command=lambda: unbind_mouse(two_sel_window),
        relief="flat"
    )
    button_2.place(
        x=585.0,
        y=489.0,
        width=258.0,
        height=61.0
    )

    reset_image = PhotoImage(
        file=relative_to_assets("reset_button.png"))
    reset_button = Button(
        image=reset_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: reset_selection(two_sel_window),
        relief="flat"
    )
    reset_button.place(
        x=4.0,
        y=4.0,
        width=34.0,
        height=34.0
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
        165.0,
        anchor="nw",
        text="Click the ‘Select Corners’",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        185.0,
        anchor="nw",
        text="button. Selecting this",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        205.0,
        anchor="nw",
        text="button will prompt the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        225.0,
        anchor="nw",
        text="program to record the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        245.0,
        anchor="nw",
        text="coordinates of the next two",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        265.0,
        anchor="nw",
        text="mouse clicks within the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        285.0,
        anchor="nw",
        text="image.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        317.0,
        anchor="nw",
        text="Select two diagonal rectangle",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        337.0,
        anchor="nw",
        text="corners.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        369.0,
        anchor="nw",
        text="Then, select ‘Initiate",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        389.0,
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
