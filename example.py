#from divoomadapter import divoom_protocol
import divoom_protocol
#from divoomadapter import divoom_device
import divoom_device
#from divoomadapter import divoom__image
import divoom_image

from PIL import Image
import time
import sys
import bluetooth

def show_files(filelist, delay=1):
	for f in filelist:
		bytes = divoom_image.image_to_divoom(f)
		pkg = thing.create_image_package(bytes)
		dev.send(pkg)
		time.sleep(delay)

def blink(filename):
	for c in range(1, 20):
		f = ""
		if (c % 2 == 0):
			f = filename
		else:
			f = "images/black.bmp"
		bytes = divoom_image.image_to_divoom(f)
		pkg = thing.create_image_package(bytes)
		dev.send(pkg)
		time.sleep(0.5)

def firework():
	basename = "images/firework"
	firework_files = []
	for n in range(1,9):
		firework_files.append(basename + str(n) + ".bmp")
	firework_files.append("images/black.bmp")
	show_files(firework_files, 0.3)
	
def firework_predefined():
	basename = "images/firework"
	firework_files = []
	for n in range(1,9):
		firework_files.append(basename + str(n) + ".bmp")
	raw_data_packages = []
	for f in firework_files:
		bytes = divoom_image.image_to_divoom(f)
		raw_data_packages.append(bytes)
	pkgs = thing.create_animation_packages(raw_data_packages, 0)
	for i in range(0, len(pkgs)):
		dev.send(pkgs[i])
		
def hello_world():
	img = divoom_image.draw_text_to_image(text="HELLO WORLD", color=divoom_image.BMP_YELLOW, size=(70, 10))
	sliced_images = divoom_image.horizontal_slices(img)
	# create divoom packages
	raw_data_packages = []
	for img in sliced_images:
		raw_data_packages.append(divoom_image.to_divoom_data(img))
	# create BT divoom packages
	pkgs = thing.create_animation_packages(raw_data_packages, 1)
	for i in range(0, len(pkgs)):
		dev.send(pkgs[i])

# ways
# 1 horizontal from left to right
# 2 vertical from upper to lower
# 3 horizontal from right to left
# 4 vertical from lower to upper
def old_to_new(old_img, new_img, way=1):

	sliced_images = divoom_image.scroll_between(old_img, new_img, way)
	pkgs = []
	# prepare the data before sending it
	for img in sliced_images:
		img_raw_bytes = divoom_image.to_divoom_data(img)
		img_bytes = thing.create_image_package(img_raw_bytes)
		pkgs.append(img_bytes)
	# send single images to divoom
	for pkg in pkgs :
		dev.send(pkg )
		time.sleep(0.1)
		
def scroll_sequence():
	img_1 = Image.open("images/example7.bmp")
	img_2 = Image.open("images/example9.bmp")
	img_3 = Image.open("images/firework6.bmp")
	img_4 = Image.open("images/example3.bmp")
	img_5 = Image.open("images/example5.bmp")

	dev.send(thing.create_temp_package())
	time.sleep(1)
	first_img_raw_bytes = divoom_image.to_divoom_data(img_1)
	first_img_bytes = thing.create_image_package(first_img_raw_bytes)
	dev.send(first_img_bytes)
	time.sleep(4)

	old_to_new(img_1, img_2, 1)
	time.sleep(1)
	old_to_new(img_2, img_3, 2)
	time.sleep(1)
	old_to_new(img_3, img_4, 3)
	time.sleep(1)
	old_to_new(img_4, img_5, 4)


DIVOMM_ADR = sys.argv[1]
thing = divoom_protocol.DivoomAuraBoxProtocol()
dev = divoom_device.DivoomDevice(DIVOMM_ADR)

dev.connect()

print("firework")
firework()

files = ["images/example.bmp", "images/example2.bmp", "images/example3.bmp", "images/example4.bmp", "images/example5.bmp", "images/example6.bmp", "images/example7.bmp", "images/example8.bmp", "images/example9.bmp"]
print("showing files")
show_files(files)

print("blinking")
blink("images/example7.bmp")

print("show time")
dev.send(thing.create_time_package())
time.sleep(10)

print("show temperature")
dev.send(thing.create_temp_package())
time.sleep(10)

print("write hello world")
hello_world()
time.sleep(10)

print("scrolling")
scroll_sequence()

print("program firework")
firework_predefined()

dev.disconnect()
