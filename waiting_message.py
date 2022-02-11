from tkinter import Tk, Canvas, Button, PhotoImage
from PIL import Image, ImageDraw
import numpy as np
import ctypes


def select_mode_main():
    # set the GUI clarity
    ctypes.windll.shcore.SetProcessDpiAwareness(3)

    # create the select mode window, link the functions for each mode
    window = Tk()

    window.geometry("300x200")
    window.configure(bg = "#A4A4A4")

    canvas = Canvas(
        window,
        bg = "#A4A4A4",
        height = 200,
        width = 300,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        15.0,
        50.0,
        anchor="nw",
        text="Selected area is too small...",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )
    # 323077-b9dec4ce-e04b-4690-ab1d-462ad0e2f003



    window.resizable(False, False)
    window.mainloop()


select_mode_main()