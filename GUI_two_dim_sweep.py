# coding=utf-8
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, END
import pandas as pd
from PIL import ImageTk
import ctypes
import Route_Demo


def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH_two_sweep = Path(__file__).parent
    ASSETS_PATH_two_sweep = OUTPUT_PATH_two_sweep / Path("./two_dim_sweep_buttons")
    return ASSETS_PATH_two_sweep / Path(path)


def get_coordinates(event):
    if len(coordinates_list) >= 2:
        coordinates_list.clear()

    coordinates_list.append([event.x-275, -1 * (event.y-300)])

    print(coordinates_list)


def bind_mouse(two_sweep_window):
    two_sweep_window.bind('<Button-1>', get_coordinates)


def unbind_mouse(two_sweep_window, entry_1):
    two_sweep_window.unbind('<Button-1>')
    del coordinates_list[1]

    print("mouse unbound")
    print(coordinates_list)

    duration = entry_1.get()
    print(duration)

    route_list = Route_Demo.two_terra(250, coordinates_list[0], 10)
    routedf = pd.DataFrame(route_list)
    routedf.to_csv('2-D Terrestrial Route.csv', index=False)
    two_sweep_window.destroy()


def main(og_window):

    og_window.destroy()

    ctypes.windll.shcore.SetProcessDpiAwareness(3)
    global coordinates_list

    coordinates_list = []

    two_sweep_window = Tk()
    two_sweep_window.geometry("900x600")
    two_sweep_window.configure(bg = "#A5A5A5")


    canvas = Canvas(
        two_sweep_window,
        bg = "#A5A5A5",
        height = 600,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        two_sweep_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: bind_mouse(two_sweep_window)
    )
    button_1.place(
        x=585.0,
        y=460.0,
        width=258.0,
        height=61.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"), master=two_sweep_window)
    button_2 = Button(
        two_sweep_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: unbind_mouse(two_sweep_window, entry_1),
        relief="flat"
    )
    button_2.place(
        x=585.0,
        y=519.0,
        width=258.0,
        height=61.0
    )

    canvas.create_text(
        588.0,
        46.0,
        anchor="nw",
        text="2-D Terrestrial Sweep",
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
        text="will scan a vertical line",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        128.0,
        anchor="nw",
        text="as the earth rotates.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        163.0,
        anchor="nw",
        text="Click the ‘Select Point’",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        183.0,
        anchor="nw",
        text="button. Selecting this",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        203.0,
        anchor="nw",
        text="button will prompt the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        223.0,
        anchor="nw",
        text="program to record the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        243.0,
        anchor="nw",
        text="coordinates of the next",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        263.0,
        anchor="nw",
        text="mouse click within the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        283.0,
        anchor="nw",
        text="image.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        319.0,
        anchor="nw",
        text="The antenna will scan the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        339.0,
        anchor="nw",
        text="maximum vertical distance at",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        560.0,
        359.0,
        anchor="nw",
        text="that point for the duration",
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
    entry_1.insert(END, 'Value between 1 & 5 hrs')
    entry_1.place(
        x=602.0,
        y=408.0+18,
        width=224.0,
        height=28.0
    )

    canvas.create_text(
        597.0,
        409.0,
        anchor="nw",
        text="Duration (hr)",
        fill="#FFFFFF",
        font=("Courier New", 18 * -1)
    )

    path = "result.png"
    img = ImageTk.PhotoImage(file=path, master=two_sweep_window)
    canvas.create_image(275, 300, image=img)

    two_sweep_window.resizable(False, False)
    two_sweep_window.mainloop()

