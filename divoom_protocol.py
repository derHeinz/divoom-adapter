import math

class DivoomAuraBoxProtocol:
	"""Creates pattern for divoom aurabox."""
	
	# static values begin and end of protocol
	PREFIX = 0x01
	POSTFIX = 0x02
	
	SINGLE_IMAGE = [0x39, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04] # single image function
	ANIMATION = [0x3b, 0x00, 0x49, 0x00, 0x0a, 0x0a, 0x04] # followed by 1-2 bytes of number (invalid byte replacement)
	
	# invalid byte processing
	INVALID_BYTES = [0x01, 0x02, 0x03]
	INVALID_BYTE_PREFIX = 0x03

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
					new_data.append(self.INVALID_BYTE_PREFIX)
					new_data.append(self.replace_byte(inv))
					break
			else:
				new_data.append(d)
		return new_data
		
	def replace_invalid_byte(self, data):
		new_data = []
		for inv in self.INVALID_BYTES:
			if (data == inv):
				new_data.append(self.INVALID_BYTE_PREFIX)
				new_data.append(self.replace_byte(inv))
				break
		else:
			new_data.append(data)
		return new_data
		
	def replace_byte(self, data):
		return (self.INVALID_BYTE_PREFIX + data)
		
	def create_animation_packages(self, data_array, time_length=0x05):
		"""Creates package for predefined animated data that will run unlimited."""
		result = []
		for i in range(0, len(data_array)):
			function = []
			function.extend(self.ANIMATION)
			function.append(i)
			function.append(time_length)
			single_package = self.create_package_for_image(function, data_array[i])
			result.append(single_package)
		return result
		
	def create_time_package(self):
		"""Creates package to let the thing show the current time."""
		return [0x01, 0x04, 0x00, 0x45, 0x00, 0x49, 0x00, 0x02]
		
	def create_temp_package(self):
		"""Creates package to let the thing show the current temperature."""
		return [0x01,0x04,0x00,0x45,0x03,0x04,0x4a,0x00,0x02]
		
	def create_set_time_package(self, hours, minutes):
		function = [0x0b, 0x00, 0x18, 0x11, 0x14, 0x0b, 0x1c]
		time = [int(hours), int(minutes)]
		post = [5, 5]
		return self.create_package(function, time + post)
	
	def create_image_package(self, data):
		"""Creates package show a single image."""
		return self.create_package_for_image(self.SINGLE_IMAGE, data)
		
	def create_package_for_image(self, function_prefix, data):
		# check data has excactly 50 bytes
		if (len(data) != 50):
			raise Exception('given data has invalid size: ' + str(len(data)))
		return self.create_package(function_prefix, data)
		
	def create_package(self, function_prefix, data):	
		# crc calculation
		crc_rel = function_prefix + data
		crc = sum(crc_rel)
		
		crc_lowerbytes = crc & 0xFF
		crc_upperbytes = crc >> 8
		
		# replace illegal bytes in data
		data2 = self.replace_invalid_bytes(data)
		function_prefix2 = self.replace_invalid_bytes(function_prefix)
		
		# construct complete package
		joined_data = [self.PREFIX] + function_prefix2 + data2
		
		# append lower and upper checksum (with invalid bytes)
		lowerbytes = self.replace_invalid_byte(crc_lowerbytes)
		joined_data.extend(lowerbytes)
		
		upperbytes = self.replace_invalid_byte(crc_upperbytes)
		joined_data.extend(upperbytes)
		
		# end token
		joined_data.append(self.POSTFIX)
		
		return joined_data
