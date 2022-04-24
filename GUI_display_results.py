# coding=utf-8
from tkinter import Tk, Canvas, Button, PhotoImage, Label
import webbrowser
from PIL import ImageTk, Image, ImageDraw, ImageFont
from pathlib import Path
import numpy as np
import imageio
import os
import glob
import shutil
from datetime import datetime

# Figma token: 332149-191bfc36-c238-4c0c-bb89-70096ed35086
# Format: tkdesigner URL TOKEN


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


def create_transparent_gif(save_path, time_list):
    """
    this function creates a gif with a black background and saves the result to the Results folder for the user
    """

    set_image_background('black_square.png', 'Results Overlays', time_list, 'white')

    # get overlay image paths from Overlays
    overlay_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results Overlays\\*')

    # make sure the overlay files are in numerical order
    overlay_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    images = []
    for file_path in overlay_files:
        images.append(imageio.imread(file_path))
        # im.show()
    kargs = {'duration': 2}

    # save the gif in the Results folder
    imageio.mimsave(save_path + '\\Results With Background.gif', images, **kargs)


def set_image_background(background_file, folder_name, time_list, color):
    """
    this function sets the background of all the overlay images as A5A5A5 gray to blend in with the display window
    """
    # open all images with a transparent background from the Overlays folder
    overlay_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays\\*')

    # make sure the overlay files are in numerical order
    overlay_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    # images = []
    # put a gray background on all of the frames
    print(overlay_files)
    for file_path in overlay_files:
        i = overlay_files.index(file_path)
        file_name = os.path.basename(file_path)
        #(file_name)
        im = Image.open(file_path).convert("RGBA")
        # im = im.convert("RGBA")
        # background.paste(im)
        # image = Image.open(file_path).convert("RGBA")
        background = Image.open(background_file).convert('RGBA')
        background.paste(im, mask=im)
        # imageio.imread(file_path)
        #images.append(background)
        # add times to the top left corner
        courier_font = ImageFont.truetype(r'C:\Users\jojok\PycharmProjects\pythonProject\HLT\cour.ttf', 25)
        add_times = ImageDraw.Draw(background)
        add_times.text((0, 0), time_list[i], font=courier_font, fill=color)
        # save the final image
        background.convert("RGB").save(folder_name + "\\Gray_" + file_name + ".png")


def create_display_gif(save_path):
    """
    this function creates a gif from the overlay images with gray background for display through the GUI
    """

    # get overlay image paths from Display Overlays
    overlay_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Display Overlays\\*')

    # make sure the overlay files are in numerical order
    overlay_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    images = []
    for file_path in overlay_files:
        images.append(imageio.imread(file_path))
        # im.show()
    # doesnt really matter since we'll adjust the timing in the tkinter display
    kargs = {'duration': 2}
    #images[0].save('Results\\Results.gif', mode='RGBA', save_all=True, append_images=images[1:], loop=0, duration=2000)

    # save the gif in the Results folder
    imageio.mimsave(save_path + '\\Results.gif', images, **kargs)


def open_results_folder():
    """
    this function opens the Results folder for the user
    """
    folder_path = 'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results'
    webbrowser.open(folder_path)


def copy_results_data(results_dir):
    """
    this function copies the frequency and magnitude data to the results folder for the user
    also copies over the Overlays folder
    """
    '''data_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data"

    # data_dir = "Z:\\Signal Data"
    # results_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results"

    # files = glob.glob('Z:\\Signal Data\\*.csv')
    files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data\\*csv')
    files_dest = results_dir + "\\Raw Data"

    for name in files:
        shutil.copy2(os.path.join(data_dir, name), files_dest)'''

    # copy over raw data files
    data_dir = "Z:\\Signal Data"
    # data_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data\\"
    data_dest = results_dir + "\\Data Files"
    shutil.copytree(data_dir, data_dest)

    # copy over data graphs
    graph_dir = "Z:\\Scan Graphs"
    # data_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data\\"
    graph_dest = results_dir + "\\Data Graphs"
    shutil.copytree(graph_dir, graph_dest)

    # copy over Overlay images
    overlay_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays"
    overlay_dest = results_dir + "\\Image Overlays"
    shutil.copytree(overlay_dir, overlay_dest)

    # copy over Overlay images with timestamps
    display_overlay_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results Overlays"
    display_overlay_dest = results_dir + "\\Image Overlays With Timestamps"
    shutil.copytree(display_overlay_dir, display_overlay_dest)

    # copy over heatmap images
    heatmap_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Heatmaps"
    heatmap_dest = results_dir + "\\Heatmaps"
    shutil.copytree(heatmap_dir, heatmap_dest)

    # copy over screenshot images
    screenshot_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots"
    screenshot_dest = results_dir + "\\Screenshots"
    shutil.copytree(screenshot_dir, screenshot_dest)

    # copy over gifs
    gif_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Display Overlays"
    gif_dest = results_dir + "\\Display Overlays"
    shutil.copytree(gif_dir, gif_dest)


def create_results_folder():
    # time_list = ['12:30:14', '12:30:24', '12:30:34', '12:30:44', '12:30:54']

    now = datetime.now()
    current_date = now.strftime("%b-%d-%Y %H-%M-%S")
    # print(current_date)

    # create a directory for that set of results
    directory = "Results " + str(current_date)
    # print(directory)
    parent_dir = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results"

    path = os.path.join(parent_dir, directory)
    # print(path)
    os.mkdir(path)

    '''create_display_gif(path)
        create_transparent_gif(path, time_list)
        copy_results_data(path)'''

    return path


def main(frame_number, time_list):
    """
    this function displays the results for the terrestrial and RPA modes
    """

    # create a directory for that set of results
    path = create_results_folder()

    # create the GUI window for this mode
    # ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # call function to change overlay images background to match the Tk root
    set_image_background('a5a5a5.png', 'Display Overlays', time_list, 'black')
    print('wrote overlay images')

    # call the function to create the display gif
    create_transparent_gif(path, time_list)
    create_display_gif(path)
    print("created display gif")

    # move magnitude and frequency data to the Results folder
    copy_results_data(path)

    root = Tk()

    root.geometry("1100x700")
    root.configure(bg="#A5A5A5")

    #frame_number = int((duration * 60) / 15) + 1
    frame_list = []

    for i in range(0, frame_number):
        index = 'gif -index {}'.format(i)
        im = Image.open(path + '\\Results.gif')
        frame = PhotoImage(file=path + '\\Results.gif', format=index)
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
        command=lambda: open_results_folder(),
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
        command=lambda: root.destroy(),
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
    """
    this function displays the results for the 2D selection mode
    """

    # create a directory for that set of results
    path = create_results_folder()

    # move magnitude and frequency data to the Results folder
    copy_results_data(path)

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
        command=lambda: open_results_folder(),
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
        command=lambda: window.destroy(),
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


#display_two_dim_sel()
'''time_list = ['12:30:14', '12:30:24', '12:30:34', '12:30:44', '12:30:54']
#test()
#create_display_gif()
create_transparent_gif(time_list)
main(5, time_list)'''
#set_image_background()
#copy_results_data()
#create_results_folder()

'''time_list = ['12:30:14', '12:30:24', '12:30:34', '12:30:44', '12:30:54']
main(5, time_list)'''

# display_two_dim_sel()
