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

'''
def clear_screenshots():
    """
    this function clears all previous screenshots from the Screenshots folder
    """
    files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\*.png')
    for f in files:
        os.remove(f)
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

'''# call the time tracker function to start taking Stellarium screenshots
stellarium_screenshots.time_tracker(hr_duration)

# after the images are taken and cropped
# check for signal data - check a value in a file?
# for now assume it is written and ready for heatmaps in the Signal Data folder
# read frequency and magnitude data into pandas dataframes
freqdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data\\freq_data.csv')
magdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Signal Data\\mag_data.csv')

# call the heatmap function with the data
# assuming that the heatmap data is in columns from left - the first scan - to right - the last scan
image_processing.two_dim_sweep(freqdf, magdf, num_scans)

# get the size of the heatmap for image overlay
heatmap_size = image_overlay.two_dim_terr_coordinates(coordinates_list)

# get cropped stellarium image paths
cropped_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped*')
# make sure they are in numerical order
cropped_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

# get heatmap image paths
heatmap_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Heatmaps\\Heatmap*')
# make sure they are in numerical order
heatmap_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))'''


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