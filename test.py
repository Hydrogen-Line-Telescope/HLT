from tkinter import Tk, Frame, Canvas
from PIL import ImageTk

t = Tk()
t.title("Transparency")

frame = Frame(t)
frame.pack()

canvas = Canvas(frame, bg="blue", width=500, height=500)
canvas.pack()

photoimage = ImageTk.PhotoImage(file="result.png")
canvas.create_image(150, 150, image=photoimage, anchor='w')

t.mainloop()


'''import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()
print(args)'''
