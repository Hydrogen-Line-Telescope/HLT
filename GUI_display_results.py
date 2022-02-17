# coding=utf-8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, END, Label
from PIL import ImageTk
import imageio
import os
import glob


def clear_folder(folder_path):
    """
    this function clears all previous screenshots from any folder
    """
    files = glob.glob(folder_path + '\\*')
    for f in files:
        os.remove(f)


def create_gif():
    # clear the Results folder
    clear_folder('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results')

    # get overlay image paths from Overlays
    overlay_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays\\*')

    # make sure the overlay files are in numerical order
    overlay_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    images = []
    for file_path in overlay_files:
        images.append(imageio.imread(file_path))
    # doesnt really matter since we'll adjust the timing in the tkinter display
    kargs = {'duration': 2}

    # save the gif in the Results folder
    imageio.mimsave('Results\\Results.gif', images, **kargs)


def main(frame_number):
    # create the GUI window for this mode
    #ctypes.windll.shcore.SetProcessDpiAwareness(2)

    root = Tk()
    root.geometry("900x600")
    root.configure(bg="#A5A5A5")

    #frame_number = int((duration * 60) / 15) + 1
    frame_list = []

    for i in range(0, frame_number):
        index = 'gif -index {}'.format(i)
        frame = PhotoImage(file='Results\\Results.gif', format=index)
        frame_list.append(frame)

    canvas = Canvas(
        root,
        bg="#A5A5A5",
        height=900,
        width=1350,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    def change_frame(number):
        if number == frame_number:
            number = 0
        label.config(image=frame_list[number])
        root.after(2000, change_frame, number + 1)

    label = Label(root)
    label.place(x=25, y=50)
    change_frame(0)

    # need to add a legend for the user and a description of the results

    root.resizable(False, False)
    root.mainloop()


def display_two_dim_sel():
    # create the GUI window for this mode
    #ctypes.windll.shcore.SetProcessDpiAwareness(2)

    root = Tk()
    root.geometry("900x600")
    root.configure(bg="#A5A5A5")

    #frame_number = int((duration * 60) / 15) + 1
    frame_list = []

    canvas = Canvas(
        root,
        bg="#A5A5A5",
        height=900,
        width=1350,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    path = "C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Overlays\\Overlay-0.png"
    img = ImageTk.PhotoImage(file=path, master=root)
    canvas.create_image(275, 300, image=img)

    # need to add a legend for the user and a description of the results

    root.resizable(False, False)
    root.mainloop()


#display_two_dim_sel()
