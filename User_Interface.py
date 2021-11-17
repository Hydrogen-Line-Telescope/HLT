import numpy as np
from PIL import Image, ImageDraw


def crop_image():
    # Open the input image as numpy array, convert to RGB
    im = Image.open('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\stellarium-000.png')
    width, height = im.size   # Get dimensions

    left = (width - 1250)/2
    top = (height - 1250)/2
    right = (width + 1250)/2
    bottom = (height + 1250)/2

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
        'C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png')

    im = Image.open('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png')
    width, height = im.size   # Get dimensions
    #print(width, height)

    new_im = im.resize((500, 500), Image.ANTIALIAS)
    width, height = im.size   # Get dimensions
    #print(width, height)
    new_im.save('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\cropped_stellarium.png', 'PNG',
                quality=100)


crop_image()
