import math


class DivoomAuraBoxFraming:
	START_OF_FRAME = 0x01
	END_OF_FRAME = 0x02
	ESCAPING_CHARACTER = 0x03

	def __init__(self):
		pass

	def create(self, value):
		frame = []
		frame.append(self.START_OF_FRAME)

		for symbol in value:
			frame += self.__escape(symbol)

		frame.append(self.END_OF_FRAME)
		return frame

	def __escape(self, value):
		if value in [self.START_OF_FRAME, self.END_OF_FRAME, self.ESCAPING_CHARACTER]:
			return [self.ESCAPING_CHARACTER, value + 0x03]
		else:
			return [value]


class DivoomAuraBoxProtocol:
	"""Creates pattern for divoom aurabox."""
	
	SINGLE_IMAGE = [0x39, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04] # single image function
	ANIMATION = [0x3b, 0x00, 0x49, 0x00, 0x0a, 0x0a, 0x04] # followed by 1-2 bytes of number (invalid byte replacement)

	def __init__(self):
		self.__framing = DivoomAuraBoxFraming()

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
		
	def create_bright_package(self):
		"""Creates package to display the current content bright."""
		return [0x01, 0x04, 0x00, 0x32, 0xd2, 0x08, 0x03, 0x04, 0x02]
		
	def create_dark_package(self):
		"""Creates package to display the current content in lower brightness."""
		return [0x01, 0x04, 0x00, 0x32, 0x3f, 0x75, 0x00, 0x02]
		
	def create_off_package(self):
		"""Creates package to disable the display (setting the brightness to 0)."""
		return [0x01, 0x04, 0x00, 0x32, 0x00, 0x36, 0x00, 0x02]
		
	def create_set_time_package(self, hours, minutes, seconds):
		function = [0x0b, 0x00, 0x18, 0x11, 0x14, 0x0b, 0x1c]
		time = [int(hours), int(minutes), int(seconds), 5]
		return self.create_package(function, time)
	
	def create_image_package(self, data):
		"""Creates package show a single image."""
		return self.create_package_for_image(self.SINGLE_IMAGE, data)
		
	def create_package_for_image(self, function_prefix, data):
		# check data has excactly 50 bytes
		if (len(data) != 50):
			raise Exception('given data has invalid size: ' + str(len(data)))
		return self.create_package(function_prefix, data)
		
	def create_package(self, function_prefix, data):	
		frame_content = function_prefix + data

		# crc calculation
		crc = sum(frame_content)
		
		crc_lowerbytes = crc & 0xFF
		crc_upperbytes = crc >> 8

		# construct complete package
		frame_content += [crc_lowerbytes, crc_upperbytes]

		# replace illegal bytes in data
		joined_data = self.__framing.create(frame_content)

		return joined_data
