from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import GUI_two_dim_area

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./error_message_buttons")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def selection_size_error():
    window = Tk()

    window.geometry("400x225")
    window.configure(bg="#A4A4A4")

    canvas = Canvas(
        window,
        bg="#A4A4A4",
        height=225,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: GUI_two_dim_area.main(window),
        relief="flat"
    )
    button_1.place(
        x=51.0,
        y=111.0,
        width=297.0,
        height=85.0
    )

    canvas.create_text(
        34.0,
        27.0001220703125,
        anchor="nw",
        text="ERROR:",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        34.0,
        43.20001220703125,
        anchor="nw",
        text="The selected area is too small.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        34.0,
        59.399993896484375,
        anchor="nw",
        text="Please restart the mode selection",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        34.0,
        75.60000610351562,
        anchor="nw",
        text="and choose a larger area.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )
    window.resizable(False, False)
    window.mainloop()
