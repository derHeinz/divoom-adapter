#from divoomadapter import divoom_protocol
import divoom_protocol
#from divoomadapter import divoom_device
import divoom_device
#from divoomadapter import read_image
import read_image
import time
import sys
import bluetooth

def show_files(filelist, delay=1):
	for f in filelist:
		bytes = read_image.image_to_divoom(f)
		pkg = thing.create_package(bytes)
		dev.send(pkg)
		time.sleep(delay)

def blink(filename):
	for c in range(1, 20):
		f = ""
		if (c % 2 == 0):
			f = filename
		else:
			f = "images/black.bmp"
		bytes = read_image.image_to_divoom(f)
		pkg = thing.create_package(bytes)
		dev.send(pkg)
		time.sleep(0.5)

def firework():
	basename = "images/firework"
	firework_files = []
	for n in range(1,9):
		firework_files.append(basename + str(n) + ".bmp")
	firework_files.append("images/black.bmp")
	show_files(firework_files, 0.3)

DIVOMM_ADR = sys.argv[1]
thing = divoom_protocol.DivoomAuraBoxProtocol()
dev = divoom_device.DivoomDevice(DIVOMM_ADR)

dev.connect()

files = ["images/example.bmp", "images/example2.bmp", "images/example3.bmp", "images/example4.bmp", "images/example5.bmp", "images/example6.bmp", "images/example7.bmp", "images/example8.bmp", "images/example9.bmp"]
show_files(files)

blink("images/example7.bmp")
firework()

dev.disconnect()
