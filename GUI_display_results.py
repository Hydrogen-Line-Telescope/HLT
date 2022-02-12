# coding=utf-8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, END, Label
import ctypes
import imageio
import os


def create_gif():
    picture_dir = 'Results'
    images = []
    for file_name in sorted(os.listdir(picture_dir)):
        if file_name.endswith('.png'):
            file_path = os.path.join(picture_dir, file_name)
            images.append(imageio.imread(file_path))
    kargs = {'duration': 2}
    imageio.mimsave('Results\\movie.gif', images, **kargs)


def main(duration):
    # create the GUI window for this mode
    root = Tk()
    root.geometry("900x600")
    root.configure(bg="#A5A5A5")

    frame_number = int((duration * 60) / 15)
    frame_list = []

    for i in range(0, frame_number):
        index = 'gif -index {}'.format(i)
        frame = PhotoImage(file='Results\\movie.gif', format=index)
        frame_list.append(frame)

    ctypes.windll.shcore.SetProcessDpiAwareness(3)

    canvas = Canvas(
        root,
        bg="#A5A5A5",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    def change_frame(number):
        if number == frame_number:
            number = 0
        label.config(image=frame_list[number])
        root.after(1000, change_frame, number + 1)

    label = Label(root)
    label.place(x=25, y=50)
    change_frame(0)

    # need to add a legend for the user and a description of the results

    root.resizable(False, False)
    root.mainloop()


main(1)
