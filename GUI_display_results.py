# coding=utf-8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, END
import ctypes
from PIL import ImageTk
from pathlib import Path

# need to add a legend for the user and a description of


def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    OUTPUT_PATH_one_sweep = Path(__file__).parent
    ASSETS_PATH_one_sweep = OUTPUT_PATH_one_sweep / Path("./two_dim_sweep_buttons")
    return ASSETS_PATH_one_sweep / Path(path)


def main():
    # remove the select mode window
    # set GUI clarity
    ctypes.windll.shcore.SetProcessDpiAwareness(3)
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

    path = "Results\\movie.gif"
    img = ImageTk.PhotoImage(file=path, master=one_sweep_window)
    canvas.create_image(275, 300, image=img)

    one_sweep_window.resizable(False, False)
    one_sweep_window.mainloop()


main()
