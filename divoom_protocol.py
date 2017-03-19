import math

class DivoomAuraBoxProtocol:
	""" creates pattern for divoom aurabox """
	PREFIX_A = [0x01]
	PREFIX_B = [0x39, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04]
	
	INVALID_BYTES = [0x01, 0x02, 0x03]

	def __init__(self):
		pass
				
	def contains_invalid_bytes(self, data):
		for invalid_byte in self.INVALID_BYTES:
			if invalid_byte in data:
				return True
		return False
		
	def replace_invalid_bytes(self, data):
		new_data = []
		for d in data:
			for inv in self.INVALID_BYTES:
				if (d == inv):
					new_data.append(0x03)
					new_data.append(self.replace_byte(inv))
					break
			else:
				new_data.append(d)
		return new_data
		
	def replace_byte(self, data):
		return (0x03 + data)

	def create_package(self, data):
		# check data has excatly 50 bytes
		if (len(data) != 50):
			raise Exception('given data has invalid size: ' + str(len(data)))
	
		# crc calculation
		crc_rel = self.PREFIX_B + data
		crc = sum(crc_rel)
		#print ("crc")
		#print (hex(crc))
		crc_lowerbytes = crc & 0xFF
		#print ("crc lowerbytes")
		#print (hex(crc_lowerbytes))
		crc_upperbytes = crc >> 8
		#print ("crc upperbytes")
		#print (hex(crc_upperbytes))
		if (crc_upperbytes in self.INVALID_BYTES):
			crc_upperbytes = self.replace_byte(crc_upperbytes)

		# check whether "wrong" bytes are contained:
		contains_invalid = self.contains_invalid_bytes(data)
		corrected_data = data
		if contains_invalid:
			corrected_data = self.replace_invalid_bytes(data)
		
		# construct complete package
		joined_data = self.PREFIX_A + self.PREFIX_B + corrected_data
		joined_data.append(crc_lowerbytes)
		if not contains_invalid: # marker 
			joined_data.append(0x03)
		joined_data.append(crc_upperbytes)
		joined_data.append(0x02)
		
		return joined_data
