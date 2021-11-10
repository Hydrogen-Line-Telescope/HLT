import GUI_two_dim_area
from tkinter import *


def new_window():
    frame = Tk()

    button_1 = Button(frame, text="Hello", command=GUI_two_dim_area.main)
    button_1.pack()

    frame.mainloop()


win = Tk()

button = Button(win, text="Click me", command=lambda: new_window())
button.pack()

win.mainloop()

'''from tkinter import *


def my_fun(event):
    print("Function called")


win = Tk()

button = Button(win, text="Click me")
button.bind("<Button-1>", my_fun)
button.pack()

win.mainloop()'''

'''from tkinter import *


def getcoordinates(event):
    global coordinates_list
    if len(coordinates_list) >= 3:
        coordinates_list.clear()

    coordinates_list.append([event.x, event.y])
    print(coordinates_list)


coordinates_list = []
root = Tk()
frame = Frame(root, width=512, height=512)
frame.bind('<Button-1>', getcoordinates)
frame.pack()
root.mainloop()'''

'''from tkinter import Tk, Frame, Canvas
from PIL import ImageTk

t = Tk()
t.title("Transparency")

frame = Frame(t)
frame.pack()

canvas = Canvas(frame, bg="blue", width=500, height=500)
canvas.pack()

photoimage = ImageTk.PhotoImage(file="result.png")
canvas.create_image(150, 150, image=photoimage, anchor='w')

t.mainloop()'''


'''import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()
print(args)'''
