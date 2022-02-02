from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from PIL import Image, ImageDraw
import numpy as np
import ctypes
import os
import glob
import GUI_two_dim_area
import GUI_two_dim_sweep
import GUI_one_dim_sweep
import GUI_repeated_point_analysis
import stellarium_screenshots

def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    # get button image files
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./select_mode_buttons")
    return ASSETS_PATH / Path(path)


def clear_screenshots():
    """
    this function clears all previous screenshots from the Screenshots folder
    """
    files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\*.png')
    for f in files:
        os.remove(f)


def crop_image():
    """
    this function takes the screenshot output by stellarium and crops the image to fit
    within the GUI as a lower quality circle
    """

    im = Image.open('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\stellarium-000.png')
    width, height = im.size   # Get dimensions

    left = (width - 1250)/2
    top = (height - 1250)/2
    right = (width + 1250)/2
    bottom = (height + 1250)/2

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
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png')

    im = Image.open('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png')
    width, height = im.size   # Get dimensions
    #print(width, height)

    new_im = im.resize((500, 500), Image.ANTIALIAS)
    width, height = im.size   # Get dimensions
    #print(width, height)
    new_im.save('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png', 'PNG',
                quality=100)


def select_mode_main():
    """
    this function:
    clears the Screenshots folder
    creates a new Stellarium screenshot at the current time
    crops that screenshot
    creates the select mode GUI window
    calls functions for each mode from the GUI buttons
    """

    '''# clear the Screenshots folder
    clear_screenshots()

    # get a current stellarium screenshot
    stellarium_screenshots.open_close_stellarium()

    # crop the stellarium image for the GUI
    crop_image()'''

    # set the GUI clarity
    ctypes.windll.shcore.SetProcessDpiAwareness(3)

    # create the select mode window, link the functions for each mode
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
        command=lambda: GUI_repeated_point_analysis.main(window),
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
        command=lambda: GUI_one_dim_sweep.main(window),
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
        text="User selects a point on the skymap.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        90.0,
        266.8000183105469,
        anchor="nw",
        text="Antenna scans a line perpendicular",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        90.0,
        284.0,
        anchor="nw",
        text="to the earth's rotation.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: GUI_two_dim_sweep.main(window),
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
        text="User selects rectangle corners.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        90.0,
        129.79998779296875,
        anchor="nw",
        text="Antenna scans the rectangular",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    canvas.create_text(
        90.0,
        146.99998474121094,
        anchor="nw",
        text="area.",
        fill="#000000",
        font=("Courier New", 16 * -1)
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: GUI_two_dim_area.main(window),
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


select_mode_main()
