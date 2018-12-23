import unittest
import divoom_framing


class TestDivoomAuraBoxFraming(unittest.TestCase):

	def setUp(self):
		self.testee = divoom_framing.DivoomAuraBoxFraming()
		pass

	def test_replace_escaping_bytes(self):
		# no replacements
		self.assertEqual(self.testee.create([0, 7]), [1, 0, 7, 2])
		self.assertEqual(self.testee.create([0, 7, 7]), [1, 0, 7, 7, 2])

		# replace
		self.assertEqual(self.testee.create([0, 1, 7]), [1, 0, 3, 4, 7, 2])
		self.assertEqual(self.testee.create([2, 3, 7]), [1, 3, 5, 3, 6, 7, 2])
		self.assertEqual(self.testee.create([2, 7]), [1, 3, 5, 7, 2])
		self.assertEqual(self.testee.create([3]), [1, 3, 6, 2])

