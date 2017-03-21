from PIL import Image

# bmp 16bit palette to divoom palett ...
# bmp pallett
# 0 = black
# 6 = green
# 7 = pink
# 9 = red
# 11 = yellow
# 12 = blue
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

REPLACER = {0:0, 6:2, 7:5, 9:1, 11:3, 12:4, 15:7}

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
		#print(str(c) + " replaced by " + str(REPLACER[c]))
		translated.append(REPLACER[c])
	result = []
	# we now have 100 values and need to have 50 bytes
	for i in range(0,100,2):
		upper = translated[i] << 4
		print("upper")
		print(translated[i])
		print(upper)
		lower = translated[i+1]
		val =  upper + lower
		result.append(val)
		
	print (result)
		
	return result

im = Image.open("example.bmp")
to_divoom_data(im)

