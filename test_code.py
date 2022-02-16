import glob

'''from PIL import Image, ImageOps, ImageDraw

im = Image.open('two_dim_terr_overlay.png')
im.show()
bigsize = (im.size[0] * 3, im.size[1] * 3)
mask = Image.new('L', bigsize, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + bigsize, fill=255)
mask = mask.resize(im.size, Image.ANTIALIAS)
im.putalpha(mask)
im.show()'''

files = glob.glob('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Screenshots\\*')
print(files)