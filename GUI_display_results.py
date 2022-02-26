# coding=utf-8
from tkinter import Tk, Canvas, Button, PhotoImage, Label
from PIL import ImageTk, Image, ImageDraw
from pathlib import Path
import numpy as np
import imageio
import os
import glob

# 332149-191bfc36-c238-4c0c-bb89-70096ed35086


def mask_image(file_path):
    im = Image.open(file_path)
    width, height = im.size  # Get dimensions

    left = (width - 1250) / 2
    top = (height - 1250) / 2
    right = (width + 1250) / 2
    bottom = (height + 1250) / 2

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
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\test.png')

    im = Image.open('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\test.png')
    width, height = im.size  # Get dimensions
    # print(width, height)

    new_im = im.resize((500, 500), Image.ANTIALIAS)
    width, height = im.size  # Get dimensions
    # print(width, height)
    new_im.save('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\test.png', 'PNG',
                quality=100)


def relative_to_assets(path: str) -> Path:
    """
    this function helps retrieve the images for the GUI buttons
    """
    OUTPUT_PATH_one_sweep = Path(__file__).parent
    ASSETS_PATH_one_sweep = OUTPUT_PATH_one_sweep / Path("./results_display_buttons")
    return ASSETS_PATH_one_sweep / Path(path)


def clear_folder(folder_path):
    """
    this function clears all previous screenshots from any folder
    """
    files = glob.glob(folder_path + '\\*')
    for f in files:
        os.remove(f)


def gen_frame(path):
    """
    function to make each frame of the gif transparent outside of the skymap
    from FelixHo
    """
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 169 if a <= 128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im


def create_gif():
    # clear the Results folder
    #clear_folder('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results')

    # get overlay image paths from Overlays
    overlay_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays\\*')

    # make sure the overlay files are in numerical order
    overlay_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    background = Image.open('a5a5a5.png')
    background = background.convert("RGBA")


    images = []
    for file_path in overlay_files:
        im = Image.open(file_path)
        im = im.convert("RGBA")
        background.paste(im)
        #im = gen_frame(file_path)
        #imageio.imread(file_path)
        images.append(im)
        im.show()
    # doesnt really matter since we'll adjust the timing in the tkinter display
    #kargs = {'duration': 2}
    images[0].save('GIF.gif', save_all=True, append_images=images[1:], loop=0, duration=2000)

    # save the gif in the Results folder
    #imageio.mimsave('Results\\Results.gif', images, **kargs)


def main(frame_number):
    # create the GUI window for this mode
    #ctypes.windll.shcore.SetProcessDpiAwareness(2)

    root = Tk()

    root.geometry("1100x700")
    root.configure(bg="#A5A5A5")

    #frame_number = int((duration * 60) / 15) + 1
    frame_list = []

    for i in range(0, frame_number):
        index = 'gif -index {}'.format(i)
        frame = PhotoImage(file='Results\\Results.gif', format=index)
        im = Image.open('Results\\Results.gif')
        print(im)
        frame_list.append(frame)

    canvas = Canvas(
        root,
        bg="#A5A5A5",
        height=700,
        width=1100,
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
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=749.0,
        y=528.0,
        width=258.0,
        height=61.0
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
        x=749.0,
        y=594.0,
        width=258.0,
        height=61.0
    )

    canvas.create_text(
        836.0,
        39.0,
        anchor="nw",
        text="Results",
        fill="#000000",
        font=("Courier New", 20 * -1)
    )

    canvas.create_text(
        724.0,
        92.0,
        anchor="nw",
        text="The image to the left shows",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        112.0,
        anchor="nw",
        text="the results of the selected",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        132.0,
        anchor="nw",
        text="antenna scan.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        169.0,
        anchor="nw",
        text="The blue areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        189.0,
        anchor="nw",
        text="Doppler blueshift in the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        209.0,
        anchor="nw",
        text="measured hydrogen emissions.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        246.0,
        anchor="nw",
        text="The red areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        266.0,
        anchor="nw",
        text="Doppler redshift in the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        286.0,
        anchor="nw",
        text="measured hydrogen emissions.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        323.0,
        anchor="nw",
        text="The purple areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        343.0,
        anchor="nw",
        text="measured hydrogen emissions",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        363.0,
        anchor="nw",
        text="closest to the hydrogen line",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        383.0,
        anchor="nw",
        text="frequency 1420.40575 MHz.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        420.0,
        anchor="nw",
        text="The intensity of each color",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        440.0,
        anchor="nw",
        text="is determined by the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        460.0,
        anchor="nw",
        text="magnitude of the measured",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        480.0,
        anchor="nw",
        text="signal.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    legend_path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\results_display_buttons\\legend_cropped.png"
    legend = ImageTk.PhotoImage(file=legend_path, master=root)
    canvas.create_image(65, 350, image=legend)

    def change_frame(number):
        if number == frame_number:
            number = 0
        label.config(image=frame_list[number])
        root.after(2000, change_frame, number + 1)

    label = Label(root, borderwidth=0)
    label.place(x=150, y=100)
    change_frame(0)

    # need to add a legend for the user and a description of the results

    root.resizable(False, False)
    root.mainloop()


def display_two_dim_sel():
    window = Tk()

    window.geometry("1100x700")
    window.configure(bg="#A5A5A5")

    canvas = Canvas(
        window,
        bg="#A5A5A5",
        height=700,
        width=1100,
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
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=749.0,
        y=528.0,
        width=258.0,
        height=61.0
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
        x=749.0,
        y=594.0,
        width=258.0,
        height=61.0
    )

    canvas.create_text(
        836.0,
        39.0,
        anchor="nw",
        text="Results",
        fill="#000000",
        font=("Courier New", 20 * -1)
    )

    canvas.create_text(
        724.0,
        92.0,
        anchor="nw",
        text="The image to the left shows",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        112.0,
        anchor="nw",
        text="the results of the selected",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        132.0,
        anchor="nw",
        text="antenna scan.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        169.0,
        anchor="nw",
        text="The blue areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        189.0,
        anchor="nw",
        text="Doppler blueshift in the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        209.0,
        anchor="nw",
        text="measured hydrogen emissions.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        246.0,
        anchor="nw",
        text="The red areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        266.0,
        anchor="nw",
        text="Doppler redshift in the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        286.0,
        anchor="nw",
        text="measured hydrogen emissions.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        323.0,
        anchor="nw",
        text="The purple areas depict the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        343.0,
        anchor="nw",
        text="measured hydrogen emissions",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        363.0,
        anchor="nw",
        text="closest to the hydrogen line",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        383.0,
        anchor="nw",
        text="frequency 1420.40575 MHz.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        420.0,
        anchor="nw",
        text="The intensity of each color",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        440.0,
        anchor="nw",
        text="is determined by the",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        460.0,
        anchor="nw",
        text="magnitude of the measured",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    canvas.create_text(
        724.0,
        480.0,
        anchor="nw",
        text="signal.",
        fill="#000000",
        font=("Courier New", 18 * -1)
    )

    legend_path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\results_display_buttons\\legend_cropped.png"
    legend = ImageTk.PhotoImage(file=legend_path, master=window)
    canvas.create_image(65, 350, image=legend)

    path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays\\Overlay-0.png"
    img = ImageTk.PhotoImage(file=path, master=window)
    canvas.create_image(400, 350, image=img)

    window.resizable(False, False)
    window.mainloop()


# mask_image('C:\\Users\\jojok\\Desktop\\2022 - Spring\\ECEN 404\\Image Processing and GUI '
           #'Images\\Results\\final_image_overlay.png')
#main(3)
#display_two_dim_sel()

create_gif()
