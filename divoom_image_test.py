import unittest
from PIL import Image
import divoom_image

class TestDivoomAuraBoxImage(unittest.TestCase):

	TESTDATA_DIR = "images/"
	
	def test_to_and_from(self):
		val = divoom_image.to_(2, 0)
		self.assertEquals((2, 0), divoom_image.from_(val))
		
		val = divoom_image.to_(1, 5)
		self.assertEquals((1, 5), divoom_image.from_(val))
		
		# this one is not excatly correct but a similar color
		val = divoom_image.to_(11, 8)
		self.assertEquals((11, 5), divoom_image.from_(val))

	def test_image_and_back_black(self):
		img = Image.open(self.TESTDATA_DIR + "black.bmp")
		divoom_data = divoom_image.to_divoom_data(img)
		img2 = divoom_image.divoom_to_image(divoom_data)
		self.assertEquals(len(img.getdata()), len(img2.getdata()))
		self.assertItemsEqual(img.getdata(), img2.getdata())
		
	def test_image_and_back_example7(self):
		img = Image.open(self.TESTDATA_DIR + "example7.bmp")
		divoom_data = divoom_image.to_divoom_data(img)
		img2 = divoom_image.divoom_to_image(divoom_data)
		
		#replace all non-unique keys
		img2data = list(img2.getdata())
		for idx, item in enumerate(img2data):
			if item == 1: # red is 9 & 1
				img2data[idx] = 9
		
		self.assertEquals(len(img.getdata()), len(img2.getdata()))
		self.assertItemsEqual(img.getdata(), img2data)
		
if __name__ == '__main__':
	unittest.main()
