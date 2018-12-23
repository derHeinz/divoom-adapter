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

