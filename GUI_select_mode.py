from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import ctypes

# get button image files
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./select_mode_buttons")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


ctypes.windll.shcore.SetProcessDpiAwareness(3)

window = Tk()

window.geometry("500x600")
window.configure(bg = "#A4A4A4")


canvas = Canvas(
    window,
    bg = "#A4A4A4",
    height = 600,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    91.0,
    517.0,
    anchor="nw",
    text="User selects a point on the skymap. ",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    91.0,
    535.0,
    anchor="nw",
    text="Antenna rotates to scan that point",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    91.0,
    552.0,
    anchor="nw",
    text="over time.",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=96.0,
    y=439.0,
    width=292.0,
    height=72.0
)

canvas.create_text(
    90.5,
    383.0,
    anchor="nw",
    text="User selects a point on the skymap. ",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.0,
    399.6000061035156,
    anchor="nw",
    text="Antenna remains stationary at that",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.5,
    417.0,
    anchor="nw",
    text="position as the earth rotates.",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=91.0,
    y=306.0,
    width=297.0,
    height=72.0
)

canvas.create_text(
    90.0,
    250.0,
    anchor="nw",
    text="User selects a point on the skymap. ",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.0,
    266.8000183105469,
    anchor="nw",
    text="Antenna scans a vertical line as",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.0,
    284.0,
    anchor="nw",
    text="the earth rotates.",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=91.0,
    y=172.0,
    width=297.0,
    height=72.0
)

canvas.create_text(
    90.0,
    113.0,
    anchor="nw",
    text="User selects diagonal rectangle ",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.0,
    129.79998779296875,
    anchor="nw",
    text="corners. Antenna scans the",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

canvas.create_text(
    90.0,
    146.99998474121094,
    anchor="nw",
    text="rectangular area.",
    fill="#000000",
    font=("Courier New", 16 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=91.0,
    y=36.0,
    width=297.0,
    height=72.0
)
window.resizable(False, False)
window.mainloop()
