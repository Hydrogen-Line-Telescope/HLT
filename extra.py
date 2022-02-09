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
print(upper_right_coord)
