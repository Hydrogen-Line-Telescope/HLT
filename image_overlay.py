# 2-dim area

# input skymap photo
# pass coordinates from the GUI
# crop skymap slightly larger than the coordinates
# input the heatmap
# overlay heatmap onto the correct skymap coordinates

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def overlay_images(heatmap_file, skymap_file, coordinates_list):
    heatmap = Image.open(heatmap_file)
    skymap = Image.open(skymap_file)
    skymap_cropped = skymap.crop(coordinates_list)
    size = skymap_cropped.size
    print(heatmap.size)
    print(skymap.size)
    print(skymap_cropped.size)

    # skymap_cropped.show()

    # make heatmap and cropped skymap the same size for blending
    heatmap = heatmap.resize(size, Image.ANTIALIAS)
    # heatmap.show()
    blended_image = Image.blend(skymap_cropped, heatmap, alpha=0.4)
    blended_image.show()


def transform_coordinates(gui_coordinates):

    crop_coordinates = []
    flat_coordinates = list(np.concatenate(gui_coordinates).flat)
    print(flat_coordinates)

    coordinates_adjusted = [i + 250 for i in flat_coordinates]
    print(coordinates_adjusted)

    for i in range(len(flat_coordinates)):
        if i % 2 == 0:
            print(i)
            print(coordinates_adjusted[i])
            print(flat_coordinates[i+1])
            crop_coordinates.append(coordinates_adjusted[i])
            crop_coordinates.append((flat_coordinates[i+1] - 250) * -1)

    # [x1, y1, x2, y2]
    # [left, bottom, right, top]
    feed_list = [crop_coordinates[0], crop_coordinates[3], crop_coordinates[2], crop_coordinates[1]]

    # crop image larger than the user's selection
    # how much bigger?
    # final_list = [i + 5 for i in feed_list]

    return feed_list


coordinates = [[-122, -68], [134, 162]]
crop_list = transform_coordinates(coordinates)
overlay_images("Heatmaps\\2-DSel.png", "Screenshots\\cropped_stellarium.png", crop_list)
