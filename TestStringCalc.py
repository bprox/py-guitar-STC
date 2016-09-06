import unittest
from StringCalc import StringCalc

class TestStringCalc(unittest.TestCase):
	def setUp(self):
		self.objSC = StringCalc()
		self.lengline = 'len 24.75"'
		self.txtlengline = 'len 24.75" == Verbose length'
		self.txtline ='C	 .013" CKPLG == 16.34#'
		self.totline = 'total == 107.5#'
		self.gauge = 0.013
		self.weight = 0.000037605
		self.wwgauge = '0.013"'
		self.length = ['len', '24.75"']
		self.lengthNoUnit = ['len', '24.75']
		self.lengthMetricCm = ['len', '62.865cm']
		self.lengthMetricMm = ['len', '628.65mm']
		self.wordndx = 0
		self.CKPLG = [
	        [.008, .000014240],
	        [.009, .000018022],
	        [.010, .000022252],
	        [.011, .000026925],
	        [.012, .000032039],
	        [.013, .000037605],
	        [.014, .000043607],
	        [.015, .000050050],
	        [.016, .000056961],
	        [.017, .000064300],
	        [.018, .000072088],
	        [.019, .000080360],
	        [.020, .000089031],
	        [.021, .000098155],
	        [.022, .000107666]]



	def test_getWeight(self):
		self.assertEqual(self.objSC.getGaugeOrWeight(self.gauge,
		self.objSC.CKPLG, 0, 1),
						0.000037605,
						 'did not properly calculate weight')


	def test_getGauge(self):
		self.assertEqual(self.objSC.getGaugeOrWeight(self.gauge, self.objSC.CKPLG, 1, 0),
						0.013,
						 'did not properly calculate gauge')

	"""
	==============================================================
	=== Test Cases for stripResults(ss) ==============
	==============================================================
	"""
	def test_stripResults_StringLine(self):
		self.assertEqual(self.objSC.stripResults(self.txtline),
						'C	 .013" CKPLG',
						 'did not strip properly')
	def test_stripResults_LengthLine(self):
		self.assertEqual(self.objSC.stripResults(self.txtlengline),
						'len 24.75"',
						 'did not strip properly')
	def test_stripResults_TotalLine(self):
		self.assertEqual(self.objSC.stripResults(self.totline),
						'total',
						 'did not strip properly')

	"""
	==============================================================
	=== Test Cases for parseGauge(word, isMetric) ================
	==============================================================
	"""
	def test_parseGauge_NoZeroDot_Inches(self):
		self.assertEqual(self.objSC.parseGauge('.013"'),
						0.013,
						 'did not properly parse gauge')
	def test_parseGauge_ZeroDot_Inches(self):
		self.assertEqual(self.objSC.parseGauge('0.013"'),
						0.013,
						 'did not properly parse gauge')
	def test_parseGauge_NoZeroDot_NoUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseGauge('.013')
	def test_parseGauge_Cm(self):
		self.assertEqual(self.objSC.parseGauge('0.03302cm'),
						0.013,
						 'did not properly parse gauge')
	def test_parseGauge_Mm(self):
		self.assertEqual(self.objSC.parseGauge('0.3302mm'),
						0.013,
						 'did not properly parse gauge')
	def test_parseGauge_NoUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseGauge('0.013')
	def test_parseGauge_BadUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseGauge('0.013btc')


	"""
	==============================================================
	=== Test Cases for parseTension(word, isMetric) ==============
	==============================================================
	"""
	def test_parseTension_PoundSign(self):
		self.assertEqual(self.objSC.parseTension('16.34#'),
						7.41143919807684,
						 'did not properly parse tension')
	def test_parseTension_Lb(self):
		self.assertEqual(self.objSC.parseTension('16.34lb'),
						7.41143919807684,
						 'did not properly parse tension')
	def test_parseTension_NoUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseTension('16.34')
	def test_parseTension_Kg(self):
		self.assertEqual(self.objSC.parseTension('7.41143919807684kg'),
						7.41143919807684,
						 'did not properly parse tension')
	def test_parseTension_BadUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseTension('16.34btc')

	"""
	==============================================================
	=== Test Cases for parseNote(word) ===========================
	==============================================================
	"""
	def test_parseNote_C_Lowercase_Oct(self):
		self.assertEqual(self.objSC.parseNote('c\'\'\''),
						39,
						 'did not properly parse note')
	def test_parseNote_A_Uppercase_Num(self):
		self.assertEqual(self.objSC.parseNote('A4'),
						0,
						 'did not properly parse note')
	def test_parseNote_A_Lowercase_Num(self):
		self.assertEqual(self.objSC.parseNote('a4'),
						0,
						 'did not properly parse note')
	def test_parseNote_A_Uppercase(self):
		self.assertEqual(self.objSC.parseNote('A'),
						0,
						 'did not properly parse note')
	def test_parseNote_A_Lowercase(self):
		self.assertEqual(self.objSC.parseNote('a'),
						12,
						 'did not properly parse note')
	def test_parseNote_D_Lowercase_Oct(self):
		self.assertEqual(self.objSC.parseNote('d,,'),
						-19,
						 'did not properly parse note')
	def test_parseNote_A_Lowercase_Oct(self):
		self.assertEqual(self.objSC.parseNote('a,,,,,'),
						-48,
						 'did not properly parse note')
	def test_parseNote_A_SharpAccent_Lowercase_Oct(self):
		self.assertEqual(self.objSC.parseNote('^a,,,,,'),
						-47,
						 'did not properly parse note')
	def test_parseNote_A_FlatAccent_Lowercase_Oct(self):
		self.assertEqual(self.objSC.parseNote('_a,,,,,'),
						-49,
						 'did not properly parse note')

	"""
	==============================================================
	=== Test Cases for parseLength(words[], wordndx, isMetric) ===
	==============================================================
	"""

	def test_parseLengthInches(self):
		self.assertEqual(self.objSC.parseLength(self.length, self.wordndx),
						62.865, 'did not properly parse length')

	def test_parseLengthNoUnit(self):
		with self.assertRaises(Exception):
			self.objSC.parseLength(self.lengthNoUnit, self.wordndx)

	def test_parseLengthMetricCm(self):
		self.assertEqual(self.objSC.parseLength(self.lengthMetricCm, self.wordndx),
						62.865, 'did not properly parse length')

	def test_parseLengthMetricMm(self):
		self.assertEqual(round(self.objSC.parseLength(self.lengthMetricMm, self.wordndx), 3),
						62.865, 'did not properly parse length')
