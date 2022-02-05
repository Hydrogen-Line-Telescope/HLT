# 2-dim area
# GUI outputs two sets of coordinates in a tuple
# rectangular area
# [[-122, -68], [134, 162]]

# 2-dim terrestrial sweep
# GUI outputs one set of coordinates in a tuple
# GUI outputs a duration in hours - link to taking stellarium pictures every 15 min
# [[-83, 2]]
# top is always 0, bottom is always 500
# 500/16/2 --> 16 pixels = 5 degrees
# x - value, add 16 pixels, subtract pixels

# 1-dim terrestrial sweep
# GUI outputs one set of coordinates in tuple
# GUI outputs a duration in hours - link to taking stellarium pictures every 15 min
# [[73, 16]]

# 1-dim terrestrial sweep
# GUI outputs one set of coordinates in tuple
# GUI outputs a duration in hours - link to taking stellarium pictures every 15 min
# [[22, 52]]

# input skymap photo
# pass coordinates from the GUI
# crop skymap slightly larger than the coordinates
# input the heatmap
# overlay heatmap onto the correct skymap coordinates


from PIL import Image, ImageDraw
import numpy as np


def image_overlay(heatmap_file, skymap_file, heatmap_size, mode):
    # open the heatmap and skymap photos
    heatmap = Image.open(heatmap_file)
    skymap = Image.open(skymap_file)

    print(heatmap_size)
    # crop the skymap according to the user's selection for 2-dim selection
    skymap_cropped = skymap.crop(heatmap_size)
    size = skymap_cropped.size

    print(heatmap.size)
    print(skymap.size)
    print(skymap_cropped.size)

    #skymap_cropped.show()

    # make heatmap and cropped skymap the same size for blending
    adjusted_heatmap = heatmap.resize(size, Image.ANTIALIAS)
    # heatmap.show()

    # blend the skymap and heatmap with an alpha value
    # decide which alpha to use
    blended_image = Image.blend(skymap_cropped, adjusted_heatmap, alpha=0.2)
    # blended_image.show()

    # paste the blended skymap and heatmap on the full skymap image at the correct coordinates
    skymap.paste(blended_image, tuple(heatmap_size))
    # skymap.show()
    img = skymap.convert("RGB")
    npImage = np.array(img)
    h, w = skymap.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    final_image = Image.fromarray(npImage)
    # final_image.show()
    final_image.resize((500, 500), Image.ANTIALIAS)
    final_image.save("Results\\final_image_overlay_" + mode + ".png")


def two_dim_sel_coordinates(gui_coordinates):

    placement_coordinates = []

    # convert user selected tuple from GUI to a list
    flat_coordinates = list(np.concatenate(gui_coordinates).flat)
    # print(flat_coordinates)

    # adjust selected corners to a coordinate system with (0, 0) in the upper left corner
    # (PIL library coordinate system)
    # adjusting x - coordinates
    coordinates_adjusted = [i + 250 for i in flat_coordinates]
    # print(coordinates_adjusted)
    # adjusting y - coordinates
    for i in range(len(flat_coordinates)):
        if i % 2 == 0:
            '''print(i)
            print(coordinates_adjusted[i])
            print(flat_coordinates[i+1])'''
            placement_coordinates.append(coordinates_adjusted[i])
            placement_coordinates.append((flat_coordinates[i+1] - 250) * -1)

    # change the order of the coordinates for PIL functions, left, bottom, right top
    # [x1, y1, x2, y2]
    # [left, top, right, bottom]
    heatmap_size = [placement_coordinates[0], placement_coordinates[3], placement_coordinates[2], placement_coordinates[1]]

    '''print("placement_coordinates", placement_coordinates)
    print("heatmap_size", heatmap_size)'''

    return heatmap_size


def two_dim_terr_coordinates(gui_coordinates):
    # take in x, y, convert to list, add / subtract 16 pixels
    # only adjusting x values
    placement_coordinates = []

    # convert user selected tuple from GUI to a list
    flat_coordinates = list(np.concatenate(gui_coordinates).flat)
    # print(flat_coordinates)

    # adjust selected corners to a coordinate system with (0, 0) in the upper left corner
    # (PIL library coordinate system)
    coordinates_adjusted = [i + 250 for i in flat_coordinates]
    # print(coordinates_adjusted)
    # adjusting y
    '''for i in range(len(flat_coordinates)):
        if i % 2 == 0:
            placement_coordinates.append(coordinates_adjusted[i])
            placement_coordinates.append((flat_coordinates[i + 1] - 250) * -1)'''

    # change the order of the coordinates for PIL functions, left, bottom, right top
    # [x1, y1, x2, y2]
    # [left, top, right, bottom]
    heatmap_size = [coordinates_adjusted[0] - 16, 0, coordinates_adjusted[0] + 16, 500]

    '''print("placement_coordinates", placement_coordinates)
    print("heatmap_size", heatmap_size)'''

    return heatmap_size


def one_dim_terr_rpa_coordinates(gui_coordinates):
    # take in x, y, convert to list, add / subtract 16 pixels
    # only adjusting x values
    placement_coordinates = []

    # convert user selected tuple from GUI to a list
    flat_coordinates = list(np.concatenate(gui_coordinates).flat)
    # print(flat_coordinates)

    # adjust selected corners to a coordinate system with (0, 0) in the upper left corner
    # (PIL library coordinate system)
    coordinates_adjusted = [i + 250 for i in flat_coordinates]

    # print(coordinates_adjusted)
    # adjusting y
    for i in range(len(flat_coordinates)):
        if i % 2 == 0:
            #placement_coordinates.append(coordinates_adjusted[i])
            placement_coordinates.append((flat_coordinates[i + 1] - 250) * -1)

    print(placement_coordinates)

    # change the order of the coordinates for PIL functions, left, bottom, right top
    # [x1, y1, x2, y2]
    # [left, top, right, bottom]
    heatmap_size = [coordinates_adjusted[0] - 16, placement_coordinates[0] - 16, coordinates_adjusted[0] + 16,
                    placement_coordinates[0] + 16]

    '''print("placement_coordinates", placement_coordinates)
    print("heatmap_size", heatmap_size)'''

    return heatmap_size


two_dim_coordinates = [[-190, -68], [134, 162]]
one_dim_coordinates = [[-83, 2]]

# get adjusted coordinates from this function
heatmap = one_dim_terr_rpa_coordinates(one_dim_coordinates)
print(heatmap)
image_overlay("Heatmaps\\1-DTS_RPA_0.png", "Screenshots\\cropped_stellarium.png", heatmap, '1d_terr')


heatmap = two_dim_terr_coordinates(one_dim_coordinates)
print(heatmap)
image_overlay("Heatmaps\\2-DTS_0.png", "Screenshots\\cropped_stellarium.png", heatmap, '2d_terr')

heatmap_two = two_dim_sel_coordinates(two_dim_coordinates)
# pass file locations for the heatmap and skymap as well as the adjusted coordinates
image_overlay("Heatmaps\\2-DSel.png", "Screenshots\\cropped_stellarium.png", heatmap_two, '2d_sel')

