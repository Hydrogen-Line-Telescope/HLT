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
    skymap_cropped = skymap.crop((3, 464, 376, 124))
    print(heatmap.size)
    print(skymap.size)
    skymap_cropped.show()

crop_coordinates = []
coordinates = [[-247, 2], [126, 214]]
flat_coordinates = list(np.concatenate(coordinates).flat)
print(flat_coordinates)

coordinates_adjusted = [i + 250 for i in flat_coordinates]
print(coordinates_adjusted)

for i, y in enumerate(flat_coordinates):
    if i % 2 == 0:
        crop_coordinates.append(coordinates_adjusted[i])
        crop_coordinates.append((y - 250) * -1)

print("cropped", crop_coordinates)

overlay_images("Heatmaps\\2-DSel.png", "Screenshots\\cropped_stellarium.png", coordinates_adjusted)
