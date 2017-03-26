from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import os
import sys

# bmp 16bit palette to divoom palett ...
# bmp pallett
BLACK = 0
# 1 = dark red
GREEN = 6
PINK = 7
# 8 = light pink
RED = 9
# 10 another yellow
YELLOW = 11
BLUE = 12
LIGHT_BLUE = 14
WHITE = 15

# divoom palette
# 0 = black
# 1 = red
# 2 = green
# 3 = yellow
# 4 = blue
# 5 = pink
# 6 = light blue
# 7 = white

REPLACER = {BLACK:0, 1:1, GREEN:2, PINK:5, 8:5, RED:1, 10:3, YELLOW:3, BLUE:4, LIGHT_BLUE:6, WHITE:7}

def pretty_print(image):
	n = 0
	for c in im.getdata():
		n=n+1
		print ("number" + str(n))
		print ("color" + str(c))
		
def to_divoom_data(image):
	# TODO check image is 10x10

	translated = []
	for c in image.getdata():
		translated.append(REPLACER[c])
	result = []
	# we now have 100 values and need to have 50 bytes
	for i in range(0,100,2):
		upper = translated[i+1] << 4
		lower = translated[i]
		val =  upper + lower
		result.append(val)
		
	return result

def image_to_divoom(iamgename):
	im = Image.open(iamgename)
	return to_divoom_data(im)
	
def horizontal_slices(image, slice_size=10):
	width, height = image.size
	slices = width - slice_size
	result_images = []
	
	for slice in range(slices):
		new_box = (slice, 0, slice+slice_size, height)
		new_img = image.crop(new_box)
		result_images.append(new_img)
	return result_images
	
def image_horizontal_slices(image_path, slice_size=10):
	img = Image.open(image_path)
	return horizontal_slices(img, slice_size)

def draw_text_to_image(text, color=RED, width=40):
	# make use of the black image to copy the palette over
	proto = Image.open(os.path.join(os.path.dirname(__file__), "images/black.bmp"))
	im = Image.new("P", (width,10))
	im.putpalette(proto.palette.getdata()[1])
	del proto
	draw = ImageDraw.Draw(im)
	fn = ImageFont.load(os.path.join(os.path.dirname(__file__),'fonts/slkscr.pil'))
	draw.text((0,0), text, font=fn, fill=color)
	del draw
	return im
