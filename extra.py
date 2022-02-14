'''from PIL import Image, ImageOps, ImageDraw
import numpy as np

# PUT THIS IN THE IMAGE_OVERLAY.PY FILE

# Open the input image as numpy array, convert to RGB
img=Image.open("image_overlay.png").convert("RGB")
npImage=np.array(img)
h,w=img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,h,w],0,360,fill=255)

# Convert alpha Image to numpy array
npAlpha=np.array(alpha)

# Add alpha layer to RGB
npImage=np.dstack((npImage,npAlpha))

# Save with alpha
final_image = Image.fromarray(npImage)
final_image.show()
final_image.resize((500, 500), Image.ANTIALIAS)
print(final_image.size)
final_image.save("final_image_overlay.png")
'''

'''
with open('Scanning_Key.txt', 'w') as f:
    f.write('1')'''

'''
import pandas as pd

df = pd.read_csv('2-D Area Route.csv')
products_list = df.values.tolist()

print(df)
print(products_list)'''

'''import os
import imageio

png_dir = 'Results'
images = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
kargs = { 'duration': 2}
imageio.mimsave('Results\\movie.gif', images, **kargs)'''
'''

coordinates_list = [[-105, 54], [130, -92]]

lower_left_coord = [0, 0]
upper_right_coord = [0, 0]

# compare x's
if coordinates_list[0][0] < coordinates_list[1][0]:
    lower_left_coord[0] = coordinates_list[0][0]
    upper_right_coord[0] = coordinates_list[1][0]
else:
    upper_right_coord[0] = coordinates_list[0][0]
    lower_left_coord[0] = coordinates_list[1][0]

# compare y's
if coordinates_list[0][1] < coordinates_list[1][1]:
    lower_left_coord[1] = coordinates_list[0][1]
    upper_right_coord[1] = coordinates_list[1][1]
else:
    upper_right_coord[1] = coordinates_list[0][1]
    lower_left_coord[1] = coordinates_list[1][1]


print(coordinates_list)
print(lower_left_coord)
print(upper_right_coord)'''

'''import tkinter as tk

root = tk.Tk()

framelist = []  # List to hold all the frames
frame_index = 0  # Frame index


while True:
    try:
        # Read a frame from GIF file
        part = 'gif -index {}'.format(frame_index)
        frame = tk.PhotoImage(file='images/animated.gif', format=part)
    except:
        last_frame = frame_index - 1  # Save index for last frame
        break  # Will break when GIF index is reached
    framelist.append(frame)
    frame_index += 1  # Next frame index


def animate(frame_number):
    if frame_number > last_frame:
        frame_number = 0
    label.config(image=framelist[frame_number])
    root.after(50, animate, frame_number + 1)


label = tk.Label(root, bg='#202020')
label.pack()

animate(0)  # Start animation

root.mainloop()
'''


def function_1():
    # assigning a string as a member of the function object
    function_1.var = "variable inside function_1"
    print("function_1 has been called")


def function_2():
    print("function_2 has been called")
    print(function_1.var)


function_1()
function_2()
