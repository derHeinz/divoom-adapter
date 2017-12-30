import unittest
import divoom_protocol

class TestDivoomAuraBoxProtocol(unittest.TestCase):

	TESTDATA_DIR = "testdata/"

	def setUp(self):
		self.testee = divoom_protocol.DivoomAuraBoxProtocol()
		pass
	
	def read_bytes(self, filename):
		file = open(self.TESTDATA_DIR + filename, 'r') 
		str = file.read()
		str_list = str.split()
		bytes_list = []
		for s in str_list:
			bytes_list.append(int(s, 16))
		return bytes_list
		
	def test_invalid_data1(self):
		data = self.read_bytes("inv_data1")
		end = self.read_bytes("inv_end1")
		test_package = self.testee.create_image_package(data)
		self.assertEquals(end, test_package)
		
	def test_invalid_data2(self):
		data = self.read_bytes("inv_data2")
		end = self.read_bytes("inv_end2")
		test_package = self.testee.create_image_package(data)
		self.assertEquals(end, test_package)
		
	def test_contains_invalid(self):
		self.assertEqual(self.testee.contains_invalid_bytes([0, 0, 7]), False)
		self.assertEqual(self.testee.contains_invalid_bytes([0, 7, 7]), False)
		self.assertEqual(self.testee.contains_invalid_bytes([7, 0]), False)
		self.assertEqual(self.testee.contains_invalid_bytes([0]), False)
		
		self.assertEqual(self.testee.contains_invalid_bytes([0, 7, 1]), True)
		self.assertEqual(self.testee.contains_invalid_bytes([0, 1, 1]), True)
		self.assertEqual(self.testee.contains_invalid_bytes([1, 0, 7]), True)
		self.assertEqual(self.testee.contains_invalid_bytes([3, 0]), True)
		self.assertEqual(self.testee.contains_invalid_bytes([2]), True)
		
	def test_replace_invalid_bytes(self):
		# no replacements
		self.assertEqual(self.testee.replace_invalid_bytes([0, 7]), [0, 7])
		self.assertEqual(self.testee.replace_invalid_bytes([0, 7, 7]), [0, 7, 7])
		
		# replace
		self.assertEqual(self.testee.replace_invalid_bytes([0, 1, 7]), [0, 3, 4, 7])
		self.assertEqual(self.testee.replace_invalid_bytes([2, 3, 7]), [3, 5, 3, 6, 7])
		self.assertEqual(self.testee.replace_invalid_bytes([2, 7]), [3, 5, 7])
		self.assertEqual(self.testee.replace_invalid_bytes([3]), [3, 6])
		
	def test_front_bytes(self):
		data = self.read_bytes("crc2")
		test_package = self.testee.create_image_package(data)
		front_bytes = test_package[:8]
		self.assertEqual(front_bytes, [0x01,0x39, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04])
		
	def test_static_last_bytes(self):
		data = self.read_bytes("crc2")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[59], 3)
		self.assertEqual(test_package[61], 2)
		
	def test_crc1(self):
		data = self.read_bytes("crc1")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-4], 0xc)
		self.assertEqual(test_package[-3], 0x03)
		self.assertEqual(test_package[-2], 0x04)
		
	def test_crc2(self):
		data = self.read_bytes("crc2")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-4], 0x55)
		self.assertEqual(test_package[-3], 0x03)
		self.assertEqual(test_package[-2], 0x05)
		
	def test_crc3(self):
		data = self.read_bytes("crc3")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-4], 0x66)
		self.assertEqual(test_package[-3], 0x03)
		self.assertEqual(test_package[-2], 0x06)
		
	def test_crc4(self):
		data = self.read_bytes("crc4")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-3], 0x4d)
		self.assertEqual(test_package[-2], 0x04)
		
	def test_check1(self):
		data = self.read_bytes("check1")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0xb) #crc
		self.assertEqual(test_package[60], 0x5) #check
		
	def test_check2(self):
		data = self.read_bytes("check2")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x2d) #crc
		self.assertEqual(test_package[60], 0x5) #check
		
	def test_check3(self):
		data = self.read_bytes("check3")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0xc) #crc
		self.assertEqual(test_package[60], 0x4) #check
		
	def test_check4(self):
		data = self.read_bytes("check4")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x13) #crc
		self.assertEqual(test_package[60], 0x4) #check
		
	def test_check5(self):
		data = self.read_bytes("check5")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x71) #crc
		self.assertEqual(test_package[60], 0x5) #check
		
	def test_check6(self):
		data = self.read_bytes("check6")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x66) #crc
		self.assertEqual(test_package[60], 0x6) #check
		
	def test_check7(self):
		data = self.read_bytes("check7")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x4b) #crc
		self.assertEqual(test_package[60], 0x4) #check
		
	def test_check8(self):
		data = self.read_bytes("check8")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[58], 0x27) #crc
		self.assertEqual(test_package[60], 0x6) #check
		
	def test_check9(self):
		data = self.read_bytes("check9")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-3], 0x47) #crc
		self.assertEqual(test_package[-2], 0x9) #check
		
	def test_check10(self):
		data = self.read_bytes("check10")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-3], 0x46) #crc
		self.assertEqual(test_package[-2], 0x9) #check
		
	def test_check11(self):
		data = self.read_bytes("check11")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-3], 0xf) #crc
		self.assertEqual(test_package[-2], 0xf) #check
		
	def test_check12(self):
		data = self.read_bytes("check12")
		test_package = self.testee.create_image_package(data)
		self.assertEqual(test_package[-4], 0x12)
		self.assertEqual(test_package[-3], 0x03)
		self.assertEqual(test_package[-2], 0x04)
		
	def test_checkanimation1(self):
		datas = [self.read_bytes("check11"), self.read_bytes("check12")]
		test_packages = self.testee.create_animation_packages(datas)
		
		# check size
		self.assertEqual(2, len(test_packages))
		
		# check package 1 prefix
		self.assertEqual(test_packages[0][1], 0x3b)
		self.assertEqual(test_packages[0][3], 0x49)
		self.assertEqual(test_packages[0][9], 0x5)
		
		# check package2 prefix
		self.assertEqual(test_packages[1][1], 0x3b)
		self.assertEqual(test_packages[1][3], 0x49)
		self.assertEqual(test_packages[1][10], 0x5)

		# check package1 numbering
		self.assertEqual(test_packages[0][8], 0x00)
		
		# check package 2 numbering (incl. invalid byte check)
		self.assertEqual(test_packages[1][8], 0x03)
		self.assertEqual(test_packages[1][9], 0x04)
		
	def test_checkanimation2(self):
		bytes_extracted = [0x01,0x3b,0x00,0x49,0x00,0x0a,0x0a,0x04,0x07,0x05,0x00,0x00,0x00,0x00,0x33,0x00,0x00,0x00,0x00,0x30,0x00,0x00,0x00,0x77,0x00,0x00,0x00,0x30,0x73,0x07,0x00,0x00,0x70,0x77,0x07,0x11,0x11,0x11,0x11,0x11,0x10,0x11,0x11,0x11,0x03,0x04,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0xaf,0x07,0x02]
		bytes_raw = [0x00,0x00,0x00,0x00,0x33,0x00,0x00,0x00,0x00,0x30,0x00,0x00,0x00,0x77,0x00,0x00,0x00,0x30,0x73,0x07,0x00,0x00,0x70,0x77,0x07,0x11,0x11,0x11,0x11,0x11,0x10,0x11,0x11,0x11,0x01,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44]

		test_packages = self.testee.create_animation_packages([bytes_raw, bytes_raw, bytes_raw, bytes_raw, bytes_raw, bytes_raw, bytes_raw, bytes_raw])
		# check size
		self.assertEqual(len(test_packages), 8)
		self.assertEqual(test_packages[7], bytes_extracted)
		
	def test_time(self):
		test_package = self.testee.create_time_package()
		self.assertEqual(test_package, [0x01, 0x04, 0x00, 0x45, 0x00, 0x49, 0x00, 0x02])
		
	def test_temp(self):
		test_package = self.testee.create_temp_package()
		self.assertEqual(test_package, [0x01,0x04,0x00,0x45,0x03,0x04,0x4a,0x00,0x02])
		
	def test_create_set_time_package(self):
		func = [0x0b, 0x00, 0x18, 0x11, 0x14, 0x0b, 0x1c]
		package_assert = [1] + func + [11, 30, 59] + [0x05, 0xd8] + [0x00,0x02]
		
		# check with ints
		test_package = self.testee.create_set_time_package(11, 30, 59)
		self.assertEqual(test_package, package_assert)

		# check with strings
		test_package = self.testee.create_set_time_package("11", "30", "59")
		self.assertEqual(test_package, package_assert)
		
if __name__ == '__main__':
	unittest.main()
