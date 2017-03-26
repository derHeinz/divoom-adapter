from PIL import Image
import math
import os

# bmp 16bit palette to divoom palett ...
# bmp pallett
# 0 = black
# 1 = dark red
# 6 = green
# 7 = pink
# 8 = light pink
# 9 = red
# 11 = yellow
# 12 = blue
# 14 = light blue
# 15 = white

# divoom palette
# 0 = black
# 1 = red
# 2 = green
# 3 = yellow
# 4 = blue
# 5 = pink
# 6 = light blue
# 7 = white

REPLACER = {0:0, 1:1, 6:2, 7:5, 8:5, 9:1, 10:3, 11:3, 12:4, 14:6, 15:7}

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
	


