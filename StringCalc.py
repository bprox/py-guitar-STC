#!/usr/bin/python
__author__ = "Brent Prox"
__license__ = "GPL"
__verson__ = "1.0.0"

from decimal import *
import sys
import re


class StringCalc():
	#static members

	def __init__(self):
		self.sep = ' == '

	def doCalculate(self, text, isVerbose, isMetric):
		#string text - contains all text from the file
		#boolean verbose - flag indicating to give more detailed info in result
		#boolean metric - flag indicating whether input/output is metric
		#this will rifle through each line and do magic

		#!!!!! use output = ''.join([output, 'ooo']) when appending
		length = 27 * 2.54
		totalTension = 0.
		output = ''
		lines = self.splitkeepsep(text, '\n') #tokenized

		for line in lines: #loop is not including newline
			if len(line) > 0 and line[0] == '\n':
				output = ''.join([output, line])
				continue

			line = self.stripResults(line)
			words = line.split()

			for wordndx, word in enumerate(words):
				pass
				#strip ':' off of word?
				if word.lower() == 'len' or word.lower() == 'length':
					try:
						output = ''.join([output, line])
						length = self.parseLength(words, wordndx, isMetric)
						rlength = length if isMetric else length / 2.54
						if isVerbose:
							output = ''.join([output, self.sep, rlength, 'cm' if isMetric else '\"'])
					except Exception, e:
						output = ''.join([output, line, self.sep, repr(e)])
					continue
				if word.lower() == 'total':
					output = ''.join([output, line, self.sep, totalTension, 'kg' if isMetric else '#'])
					totalTension = 0.
					continue
				if word.lower() == 'totalx2':
					output = ''.join([output, line, self.sep, (totalTension * 2), 'kg' if isMetric else '#'])
					totalTension = 0.
					continue
				else:
					#looking at a note
					note = 0
					tension, gauge = 0.
					doTension = True

					try:
						note = parseNote(word)
					except Exception, e:
						output = ''.join([output, line, self.sep, repr(e)])

					#get next word of string line
					#** might have to rethink this, need to get next word in list of words
					#	but dont want to keep referencing them by index :\

			break #next line please
		return output
		pass

	def splitkeepsep(self, s, sep):
		return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

	def stripResults(self, ss):
		#string ss - is the line being viewed
		#strip off ' == ' and all following text
		pass
		indx = ss.rfind(self.sep)
		if indx >= 0:
			return ss[:indx]
		else:
			return ss

	def getWeight(self, gauge, weights):
		#double gauge - the gauge parsed from text
		# weights - the weight data 2d array (gauge, weight)
		#calls getGaugeOrWeight with specific params
		pass

	def getGauge(self, weight, weights):
		#double weight - the weight parsed from text
		#double[][] weights - the weight data 2d array (gauge, weight)
		#calls getGaugeOrWeight with specific params
		pass

	def getGaugeOrWeight(self, value, weights, inndx, outdx):
		#double value - the gauge or weight value passed in from getWeight() or getGauge()
		#double[][] weights - the weight data 2d array (gauge, weight)
		#int inndx - indicates the column that the value is (gauge/weight)
		#int outdx - indicates the column where the passed in value's mapped value is
		pass

	def parseGauge(self, ww):
		#string ww - the word being looked at from the line of text
		#returns gauge diameter in inches
		pass
		for ii , c in enumerate(ww):
			if c != '.' and not c.isdigit():
				break
		if ii < len(ww):
			dd = float(ww[:ii]) #get length value without unit
			ww = ww[ii:] #grab unit
			if ww == '\"': pass
			elif ww == 'cm':
				dd /= 2.54 #convert gauge diameter to inches
			elif ww == 'mm':
				dd /= 25.4 #convert gauge diameter to inches
			else:
				raise Exception('Invalid gauge unit (use \", cm, or mm)')
		else: #no unit given
			raise Exception('Invalid gauge unit (use \", cm, or mm)')
		return round(dd, 14)

	def parseTension(self, ww):
		#string ww - the word being looked at from the line of text
		#returns tension in kg
		pass
		for ii , c in enumerate(ww):
			if c != '.' and not c.isdigit():
				break
		if ii < len(ww):
			dd = float(ww[:ii]) #get length value without unit
			ww = ww[ii:] #grab unit
			if ww == '#' or ww == 'lb':
				dd /= 2.2047 #convert to kg
			elif ww == 'kg': pass #allow kg
			else:
				raise Exception('Invalid tension unit (use kg, #, or lb)')
		else: #no unit given
			raise Exception('Invalid tension unit (use kg, #, or lb)')
		return round(dd, 14)


	def parseNote(self, ww):
		#string ww - the word being looked at from the line of text
		#returns note number - A440 is the base with note# 0
		pass
		accidental = 0
		if ww[0] == '_':
			accidental  = -1
			ww = ww[1:]
		elif ww[0] == '^':
			accidental = 1
			ww = ww[1:]

		note =  "C D EF G A Bc d ef g a b".index(ww[0])
		if note == -1:
			raise Exception('Invalid Note')
		ww = ww[1:] #strip note letter
		if len(ww) > 0: #but wait! there's more!
			if ww[0].isdigit(): # e.g 7 or 4 for B7 or A4
				if note >= 12: #note is lower case
					note -= 12 #treat note as uppercase (middle octave) i.e. a7 = A7
				note += 12 * (int(ww[0]) - 4) #take octave digit
				ww = ww[1:] #strip number
			else: #its an octave identifier
				while len(ww) > 0 and ww[0] == ',': #check for lower octave
					note -= 12
					ww = ww[1:] # strip octave identifier
				while len(ww) > 0 and ww[0] == '\'': #check for higher octave
					note += 12
					ww = ww[1:] # strip octave identifier
		if len(ww) > 0:
			if ww[0] == 'b': #flat
				accidental = -1
				ww = ww[1:]
			elif ww[0] == '#': #sharp
				accidental = 1
				ww = ww[1:]
		if len(ww) > 0:
			raise Exception('Invalid Note')
		note += accidental #set accidental
		note -= 9 # A440 is base i.e. if note is A4 note = 0, if E4 note = -5
		return note


	def parseLength(self, words, wordndx):
		#StringTokenizer words - lines of text delimited by space
		#boolean metric - flag indicating input/output is in metric
		#returns scale length in cm - runs through the tokenized line of text
		pass
		ww = words[wordndx + 1]
		for ii, c in enumerate(ww):
			if c != '.' and not c.isdigit():
				break
		dd = float(ww[:ii]) #get length value without unit
		if ii < len(ww):
			ww = ww[ii:] #grab unit
		elif wordndx + 2 <= len(words):
			ww = words[wordndx + 2] #grab unit seprated by space
		else:
			raise Exception('Invalid length unit (use \", cm, or mm)')

		if ww == '\"':
			dd *= 2.54 #convert to cm
		elif ww == 'cm': pass
		elif ww == 'mm': #convert to cm
			dd /= 10.0
		else:
			raise Exception('Invalid length unit (use \", cm, or mm)') #throw Exception

		return dd


	# Circle K String weight datas
	CKPLB = [
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
		[.022, .000107666],
		[.023, .000117702]]

	CKPLG = [
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

	CKWNG = [
        [.021, .000093873],
        [.022, .000103500],
        [.023, .000113985],
        [.024, .000124963],
        [.025, .000136054],
        [.026, .000144691],
        [.027, .000153146],
        [.028, .000161203],
        [.029, .000178551],
        [.031, .000198902],
        [.033, .000223217],
        [.035, .000249034],
        [.037, .000276237],
        [.039, .000304788],
        [.041, .000334965],
        [.043, .000366357],
        [.045, .000404956],
        [.047, .000447408],
        [.049, .000475438],
        [.051, .000512645],
        [.053, .000551898],
        [.055, .000584407],
        [.057, .000625704],
        [.059, .000679149],
        [.061, .000720293],
        [.063, .000765973],
        [.065, .000821116],
        [.067, .000870707],
        [.070, .000939851],
        [.073, .001021518],
        [.076, .001110192],
        [.079, .001188974],
        [.082, .001293598],
        [.086, .001416131],
        [.090, .001544107],
        [.094, .001677765],
        [.098, .001831487],
        [.102, .001986524],
        [.106, .002127413],
        [.112, .002367064],
        [.118, .002616406],
        [.124, .002880915],
        [.130, .003154996],
        [.136, .003441822],
        [.142, .003741715],
        [.150, .004051506],
        [.158, .004375389],
        [.166, .005078724],
        [.174, .005469937],
        [.182, .006071822],
        [.190, .006605072],
        [.200, .007311717],
        [.210, .008037439],
        [.222, .009091287],
        [.232, .009888443],
        [.244, .010907182],
        [.254, .011787319]]

	CKWNB = [
        [.025, .000124568],
        [.026, .000144691],
        [.027, .000153146],
        [.028, .000161203],
        [.029, .000178551],
        [.031, .000198902],
        [.033, .000223217],
        [.035, .000249034],
        [.037, .000276237],
        [.039, .000304788],
        [.041, .000334965],
        [.043, .000366357],
        [.045, .000404956],
        [.047, .000447408],
        [.049, .000475438],
        [.051, .000512645],
        [.053, .000551898],
        [.055, .000584407],
        [.057, .000625704],
        [.059, .000679149],
        [.061, .000720293],
        [.063, .000765973],
        [.065, .000821116],
        [.067, .000870707],
        [.070, .000939851],
        [.073, .001021518],
        [.076, .001110192],
        [.079, .001188974],
        [.082, .001293598],
        [.086, .001416131],
        [.090, .001544107],
        [.094, .001677765],
        [.098, .001831487],
        [.102, .001986524],
        [.106, .002127413],
        [.112, .002367064],
        [.118, .002616406],
        [.124, .002880915],
        [.130, .003154996],
        [.136, .003441822],
        [.142, .003741715],
        [.150, .004051506],
        [.158, .004375389],
        [.166, .005078724],
        [.174, .005469937],
        [.182, .006071822],
        [.190, .006605072],
        [.200, .007311717],
        [.210, .008037439],
        [.222, .009091287],
        [.232, .009888443],
        [.244, .010907182],
        [.254, .011787319]]

	DAPL = [
        [.007, .00001085],
        [.008, .00001418],
        [.0085, .00001601],
        [.009, .00001794],
        [.0095, .00001999],
        [.010, .00002215],
        [.0105, .00002442],
        [.011, .00002680],
        [.0115, .00002930],
        [.012, .00003190],
        [.013, .00003744],
        [.0135, .00004037],
        [.014, .00004342],
        [.015, .00004984],
        [.016, .00005671],
        [.017, .00006402],
        [.018, .00007177],
        [.019, .00007997],
        [.020, .00008861],
        [.022, .00010722],
        [.024, .00012760],
        [.026, .00014975]]

	DAPB = [
        [.020, .00008106],
        [.021, .00008944],
        [.022, .00009876],
        [.023, .00010801],
        [.024, .00011682],
        [.025, .00012686],
        [.026, .00013640],
        [.027, .00014834],
        [.029, .00017381],
        [.030, .00018660],
        [.032, .00021018],
        [.034, .00023887],
        [.035, .00025365],
        [.036, .00026824],
        [.039, .00031124],
        [.042, .00036722],
        [.045, .00041751],
        [.047, .00045289],
        [.049, .00049151],
        [.052, .00055223],
        [.053, .00056962],
        [.056, .00063477],
        [.059, .00070535],
        [.060, .00073039],
        [.062, .00077682],
        [.064, .00082780],
        [.066, .00087718],
        [.070, .00096833]]

	DAXSG = [
        [.018, .00006153],
        [.020, .00007396],
        [.021, .00008195],
        [.022, .00009089],
        [.024, .00010742],
        [.026, .00012533],
        [.028, .00014471],
        [.030, .00017002],
        [.032, .00019052],
        [.034, .00021229],
        [.036, .00023535],
        [.038, .00025969],
        [.040, .00028995],
        [.042, .00031685],
        [.046, .00037449],
        [.048, .00040523],
        [.050, .00043726],
        [.052, .00047056],
        [.054, .00052667],
        [.056, .00056317],
        [.070, .00087444]]

	DANW = [
        [.017, .00005524],
        [.018, .00006215],
        [.019, .00006947],
        [.020, .00007495],
        [.021, .00008293],
        [.022, .00009184],
        [.024, .00010857],
        [.026, .00012671],
        [.028, .00014666],
        [.030, .00017236],
        [.032, .00019347],
        [.034, .00021590],
        [.036, .00023964],
        [.038, .00026471],
        [.039, .00027932],
        [.042, .00032279],
        [.044, .00035182],
        [.046, .00038216],
        [.048, .00041382],
        [.049, .00043014],
        [.052, .00048109],
        [.056, .00057598],
        [.059, .00064191],
        [.060, .00066542],
        [.062, .00070697],
        [.064, .00074984],
        [.066, .00079889],
        [.068, .00084614],
        [.070, .00089304],
        [.072, .00094124],
        [.074, .00098869],
        [.080, .00115011]]

	DAHRG = [
        [.022, .00011271],
        [.024, .00013139],
        [.026, .00015224],
        [.030, .00019916],
        [.032, .00022329],
        [.036, .00027556],
        [.039, .00032045],
        [.042, .00036404],
        [.046, .00043534],
        [.052, .00054432],
        [.056, .00062758]]

	DACG = [
        [.020, .00007812],
        [.022, .00009784],
        [.024, .00011601],
        [.026, .00013574],
        [.028, .00014683],
        [.030, .00016958],
        [.032, .00019233],
        [.035, .00024197],
        [.038, .00026520],
        [.040, .00031676],
        [.042, .00034377],
        [.045, .00040393],
        [.048, .00043541],
        [.050, .00047042],
        [.052, .00049667],
        [.056, .00059075],
        [.065, .00089364]]

	DAFT = [
        [.023, .00012568],
        [.024, .00013651],
        [.026, .00015894],
        [.028, .00017209],
        [.030, .00019785],
        [.032, .00023852],
        [.035, .00027781],
        [.036, .00029273],
        [.039, .00032904],
        [.042, .00036219],
        [.044, .00041047],
        [.045, .00042603],
        [.047, .00046166],
        [.053, .00055793],
        [.056, .00064108]]

	DABW = [
        [.020, .00007862],
        [.021, .00008684],
        [.022, .00009600],
        [.023, .00010509],
        [.024, .00011353],
        [.025, .00012339],
        [.026, .00013253],
        [.027, .00014397],
        [.029, .00016838],
        [.030, .00018092],
        [.032, .00020352],
        [.034, .00022752],
        [.035, .00024006],
        [.036, .00025417],
        [.039, .00030063],
        [.042, .00034808],
        [.045, .00040245],
        [.047, .00043634],
        [.049, .00047368],
        [.052, .00053224],
        [.053, .00054852],
        [.056, .00061132],
        [.059, .00068005]]

	DAZW = [
        [.022, .00009802],
        [.024, .00011594],
        [.025, .00012592],
        [.026, .00013536],
        [.030, .00018507],
        [.032, .00020839],
        [.034, .00023316],
        [.035, .00024610],
        [.036, .00026045],
        [.040, .00032631],
        [.042, .00035735],
        [.044, .00038985],
        [.045, .00040665],
        [.046, .00042565],
        [.050, .00050824],
        [.052, .00054686],
        [.054, .00058694],
        [.056, .00062847]]

	DAXB = [
        [.018, .00007265],
        [.020, .00009093],
        [.028, .00015433],
        [.042, .00032252],
        [.052, .00051322],
        [.032, .00019000],
        [.035, .00022362],
        [.040, .00029322],
        [.045, .00037240],
        [.050, .00046463],
        [.055, .00054816],
        [.060, .00066540],
        [.065, .00079569],
        [.070, .00093218],
        [.075, .00104973],
        [.080, .00116023],
        [.085, .00133702],
        [.090, .00150277],
        [.095, .00169349],
        [.100, .00179687],
        [.105, .00198395],
        [.110, .00227440],
        [.120, .00250280],
        [.125, .00274810],
        [.130, .00301941],
        [.135, .00315944],
        [.145, .00363204]]

	DAHB = [
        [.030, .00019977],
        [.040, .00031672],
        [.045, .00039328],
        [.050, .00046898],
        [.055, .00058122],
        [.060, .00070573],
        [.065, .00080500],
        [.070, .00096476],
        [.075, .00103455],
        [.080, .00118785],
        [.085, .00138122],
        [.090, .00140885],
        [.095, .00166888],
        [.100, .00185103],
        [.105, .00205287],
        [.110, .00220548],
        [.130, .00301941]]

	DABC = [
        [.040, .00032716],
        [.045, .00039763],
        [.050, .00047855],
        [.055, .00056769],
        [.060, .00070108],
        [.065, .00080655],
        [.070, .00093374],
        [.075, .00100553],
        [.080, .00120719],
        [.085, .00138675],
        [.090, .00148896],
        [.095, .00173288],
        [.100, .00189041],
        [.105, .00204302],
        [.110, .00226455],
        [.132, .00314193]]

	DABS = [
        [.032, .00020465],
        [.040, .00029409],
        [.045, .00036457],
        [.050, .00042635],
        [.055, .00058296],
        [.060, .00067781],
        [.065, .00073365],
        [.070, .00087014],
        [.075, .00095857],
        [.080, .00111879],
        [.085, .00124034],
        [.090, .00151382],
        [.095, .00156550],
        [.100, .00169349],
        [.105, .00183626],
        [.110, .00218579],
        [.125, .00263432],
        [.130, .00277435],
        [.145, .00327321]]

	# more helper functions will go here
	# trust me, they'll be the best

def readFromFile(filename, mode):
	f = open(filename, mode) #open file
	return f.read()

def writeToFile(filetext):
	pass

def main():
	verbose = sys.argv[1] == 'True'
	metric = sys.argv[2] == 'True'

	objSC = StringCalc()
	intxt = readFromFile('test.txt', 'r+')
	outtxt = objSC.doCalculate(intxt, verbose, metric)
	print outtxt




if __name__ == "__main__":
		main()
else:
		pass
