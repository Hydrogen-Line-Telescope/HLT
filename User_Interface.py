import numpy as np
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

# Open the input image as numpy array, convert to RGB

im = Image.open('C:\\Users\\jojok\\Pictures\\Stellarium\\stellarium-021.png')
width, height = im.size   # Get dimensions

left = (width - 1250)/2
top = (height - 1250)/2
right = (width + 1250)/2
bottom = (height + 1250)/2

# Crop the center of the image
im = im.crop((left, top, right, bottom))

img=im.convert("RGB")
npImage=np.array(img)
h,w=img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size, 0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0, 0, h, w], 0, 360, fill=255)

# Convert alpha Image to numpy array
npAlpha = np.array(alpha)

# Add alpha layer to RGB
npImage = np.dstack((npImage, npAlpha))

# Save with alpha
Image.fromarray(npImage).save('result.png')

im = Image.open('result.png')
width, height = im.size   # Get dimensions
print(width, height)

new_im = im.resize((600, 600), Image.ANTIALIAS)
width, height = im.size   # Get dimensions
print(width, height)
new_im.save('result.png', 'PNG', quality=100)

#This creates the main window of an application
window = tk.Tk()
window.title("Join")
window.geometry("800x600")
window.configure(background='grey')

path = "result.png"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "left", fill = "both", expand = "no")

#Start the GUI
window.mainloop()



'''from PIL import Image
im = Image.open('C:\\Users\\jojok\\Pictures\\Stellarium\\stellarium-021.png')
width, height = im.size   # Get dimensions

print(width, height)


left = (width - 1300)/2
top = (height - 1300)/2
right = (width + 1300)/2
bottom = (height + 1300)/2

# Crop the center of the image
im = im.crop((left, top, right, bottom))

im.save('test_crop.png', 'PNG')'''
