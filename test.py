import glob
from PIL import Image, ImageDraw
import numpy as np
import image_processing as im_proc
import pandas as pd
import image_overlay
import GUI_display_results

def crop_image(im, num_image):
    """
    this function takes the screenshot output by stellarium and crops the image to fit
    within the GUI as a lower quality circle
    """

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
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png')

    im = Image.open(
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png')
    width, height = im.size  # Get dimensions
    # print(width, height)

    new_im = im.resize((500, 500), Image.ANTIALIAS)
    width, height = im.size  # Get dimensions
    # print(width, height)
    # cropped images labeled as cropped_stellarium-#.png
    new_im.save(
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped-' + num_image + '.png',
        'PNG',
        quality=100)


'''files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\*')

# make sure the list of files is in ascending order by the number of the screenshot
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
for i in range(0, len(files)):
    print(files[i])
    image = Image.open(files[i])
    # pass the image and image number to the crop_image function
    crop_image(image, str(i))'''

'''num_scans = 4
coordinates_list = [[-83, 2]]

heatmap_size = image_overlay.two_dim_terr_coordinates(coordinates_list)

# get cropped stellarium image paths
cropped_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\Cropped*')
# make sure they are in numerical order
cropped_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

# get heatmap image paths
heatmap_files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Heatmaps\\Heatmap*')
# make sure they are in numerical order
heatmap_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

for i in range(0, num_scans):
    image_overlay.image_overlay(heatmap_files[i], cropped_files[i], heatmap_size, str(i))'''

GUI_display_results.create_gif()
GUI_display_results.main(1)


'''picture_dir = 'Results'
    images = []
    for file_name in overlay_files:
        if file_name.endswith('.png'):
            file_path = os.path.join(picture_dir, file_name)
            images.append(imageio.imread(file_path))
    kargs = {'duration': 2}
    imageio.mimsave('Results\\movie.gif', images, **kargs)'''