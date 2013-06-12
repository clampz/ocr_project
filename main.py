#!/usr/bin/python

"""
  main.py
  by David Weinman
  4/23/13, 3:25a
"""

import sys
from neuralNet import *
from propagate import *
from file import *

# these are string constants for neural net and training printouts
mapTitle = "=================================\nNeural Net Map\n================================="
backPropTitle = "=================================\nBack Propagation\n================================="
propLoopTitle = "---------------------------------\nBack Propagation (Loop: %d)\n---------------------------------"

# dictionary of params for the neural net training algorithm
dStruct = {
	'input' : [],
	'max_iterations' : 0,
	'error_threshhold' : 0,
	'n_inputs' : 0,
	'n_outputs' : 0,
	'n_hiddenLayers' : 0,
	'neuronsInHidden' : [],
	'rateOfLearning' : 0,
	'target' : 0
}

"""
indentation object for net printout
"""
class indent():
	indentorUnit = ''
	outputString = ''

	def __init__(self, unit):
		self.indentorUnit = unit
		self.outputString = ''

	# makes it bigger
	def increment(self):
		self.outputString = self.outputString + self.indentorUnit
		return self.outputString

	# returns current string
	def currentString(self):
		return self.outputString

	# makes it smaller
	def decrement(self):
		self.outputString = self.outputString[0:(len(self.outputString) - len(self.indentorUnit))]
		return self.outputString

"""
basic hash function. takes a string to search with (string),
and a dictionary object (dictionary) and returns a boolean
represenation of whether the key is in the dictionary.
"""
def hasKey(string, dictionary):
	if string in dictionary.keys():
		return True
	return False

"""
sorts the options and calls appropriate functions respectively

python main.py -r params.dat neuralNets.dat 2
python main.py -t params.dat
python main.py --help
"""
def main():
	if (sys.argv[1] == "-r"):
		if (not len(sys.argv) == 5):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 4, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[2])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		runNeuralNet(sys.argv[3], eval(sys.argv[4]))
	elif (sys.argv[1] == "-t"):
		if (not len(sys.argv) == 3):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 2, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[2])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		trainNeuralNet()
	elif (sys.argv[1] == "--help"):
		print("\nexamples:\npython main.py -r params.dat neuralNets.dat 2\npython main.py -t params.dat\n")
	else:
		raise ValueError('main.py: invalid option specified: %s' % sys.argv[1])
	return

"""
takes a filename to get the neural net weights from (neuralNetFile)
and a line number to look for the weights at (neuralNetLineNum)
"""
def runNeuralNet(neuralNetFile, neuralNetLineNum):
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])
	loadNeuralNet(inputNeuralNet, neuralNetFile, neuralNetLineNum)
	answer = eval(raw_input('do you want to run some input on the neural net? (enter True or False): '))
	while (answer):
		print("output:\n%s" % inputNeuralNet.update(dStruct['input'][eval(raw_input('which input do you want to use from the input patterns?(enter an int): '))]))
		print("\n\n\done ..\n\n")
		answer = eval(raw_input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
	return

"""
takes no params and trains the neural net, asks if the user wants to
save the weights somewhere.
"""
def trainNeuralNet():
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])

# I'm testing the neural nets with fixed weights to start off with right now, so the loop below fixes the weights.
	#for i in inputNeuralNet.layers[0].neurons:
	#	i.putWeights([.5, .5])

	backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
	print('ok, so my neural net has %.20f rate of learning and %.20f error threshhold' % (dStruct['rateOfLearning'], dStruct['error_threshhold']))
	answer = eval(raw_input('do you want to run some input on the neural net? (enter True or False): '))
	while (answer):
		print("output:\n%s" % inputNeuralNet.update(dStruct['input'][eval(raw_input('which input do you want to use from the input patterns?(enter an int): '))]))
		print("\n\n\done ..\n\n")
		answer2 = eval(raw_input('\nok .. liek ... do you want to save your neural net? (enter True or False): '))
		if answer2:
			filename = raw_input('\nok .. liek ... what is your filename?: ')
			lineNo = saveNeuralNet(inputNeuralNet, filename)
			print("\nthe line number it got saved at is: %d" % lineNo)
		answer = eval(raw_input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
	return

if __name__ == "__main__": main()

""" JUNK
=================================
=================================
---------------------------------
---------------------------------

	if (not len(sys.argv) == 2):
		raise ValueError('Main.py: wrong number of command line arguments. Asks for 1, %d given.' % (len(sys.argv) - 1))
	datas = getDataFromFile(sys.argv[1])
	for i in datas:
		if hasKey(i[0], dStruct):
			dStruct[i[0]] = eval(i[1])
	print dStruct
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])

# I'm testing the neural nets with fixed weights to start off with right now, so the loop below fixes the weights.
	#for i in inputNeuralNet.layers[0].neurons:
	#	i.putWeights([.5, .5])

	backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
	print('ok, so my neural net has %.20f rate of learning and %.20f error threshhold' % (dStruct['rateOfLearning'], dStruct['error_threshhold']))

#py ver3 code
	#answer = eval(input('do you want to run some input on the neural net? (enter True or False): '))

#py ver 2.7 code
	answer = eval(raw_input('do you want to run some input on the neural net? (enter True or False): '))
	while (answer):
#py ver 2.7 code
		print("output:\n%s" % inputNeuralNet.update(dStruct['input'][eval(raw_input('which input do you want to use from the input patterns?(enter an int): '))]))
#py ver3 code
		#print("output:\n%s" % inputNeuralNet.update(dStruct['input'][eval(input('which input do you want to use from the input patterns?(enter an int): '))]))
		print("\n\n\done ..\n\n")
#py ver 2.7 code
		answer = eval(raw_input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
#py ver3 code
		#answer = eval(input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
"""
