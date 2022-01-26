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
    print(heatmap.size)
    print(skymap.size)


coordinates = [[-134, -112], [131, 157]]
overlay_images("Heatmaps\\2-DSel.png", "cropped_stellarium.png", coordinates)
