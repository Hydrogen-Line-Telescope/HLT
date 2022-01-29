from PIL import Image, ImageOps, ImageDraw
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
