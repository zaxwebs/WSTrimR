from PIL import Image, ImageChops
import os

def trim(im, color):
    bg = Image.new(im.mode, im.size, color)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

color = (255,255,255)

for filename in os.listdir('src'):
	if filename.lower().endswith('.png'):
		color = (255,255,255, 0)
	im = Image.open('src/'+filename)
	im = trim(im, color)
	im.save('dist/'+filename)