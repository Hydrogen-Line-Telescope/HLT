# 2-dim area

# input skymap photo
# pass coordinates from the GUI
# crop skymap slightly larger than the coordinates
# input the heatmap
# overlay heatmap onto the correct skymap coordinates

from PIL import Image
import numpy as np


def overlay_images(heatmap_file, skymap_file, heatmap_size):
    # open the heatmap and skymap photos
    heatmap = Image.open(heatmap_file)
    skymap = Image.open(skymap_file)

    # crop the skymap according to the user's selection for 2-dim selection
    skymap_cropped = skymap.crop(heatmap_size)
    size = skymap_cropped.size

    '''print(heatmap.size)
    print(skymap.size)
    print(skymap_cropped.size)'''

    # skymap_cropped.show()

    # make heatmap and cropped skymap the same size for blending
    adjusted_heatmap = heatmap.resize(size, Image.ANTIALIAS)
    # heatmap.show()

    # blend the skymap and heatmap with an alpha value
    # decide which alpha to use
    blended_image = Image.blend(skymap_cropped, adjusted_heatmap, alpha=0.2)
    # blended_image.show()

    # paste the blended skymap and heatmap on the full skymap image at the correct coordinates
    skymap.paste(blended_image, tuple(heatmap_size))
    skymap.show()


def transform_coordinates(gui_coordinates):

    placement_coordinates = []

    # convert user selected tuple from GUI to a list
    flat_coordinates = list(np.concatenate(gui_coordinates).flat)
    # print(flat_coordinates)

    # adjust selected corners to a coordinate system with (0, 0) in the upper left corner
    # (PIL library coordinate system)
    coordinates_adjusted = [i + 250 for i in flat_coordinates]
    # print(coordinates_adjusted)
    for i in range(len(flat_coordinates)):
        if i % 2 == 0:
            print(i)
            print(coordinates_adjusted[i])
            print(flat_coordinates[i+1])
            placement_coordinates.append(coordinates_adjusted[i])
            placement_coordinates.append((flat_coordinates[i+1] - 250) * -1)

    # change the order of the coordinates for PIL functions, left, bottom, right top
    # [x1, y1, x2, y2]
    # [left, bottom, right, top]
    heatmap_size = [placement_coordinates[0], placement_coordinates[3], placement_coordinates[2], placement_coordinates[1]]

    '''print("placement_coordinates", placement_coordinates)
    print("heatmap_size", heatmap_size)'''

    return heatmap_size


coordinates = [[-122, -68], [134, 162]]
# get adjusted coordinates from this function
heatmap = transform_coordinates(coordinates)

# pass file locations for the heatmap and skymap as well as the adjusted coordiantes
overlay_images("Heatmaps\\2-DSel.png", "Screenshots\\cropped_stellarium.png", heatmap)
