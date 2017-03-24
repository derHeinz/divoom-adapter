from PIL import Image

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
	# check image is 10x10

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
