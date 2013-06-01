#!/usr/bin/python

"""
  main.py
  by David Weinman
  4/23/13, 3:25a
"""

import sys
from neuralNet import *
from propagate import *
from fileReader import *

"""
=================================
=================================
---------------------------------
---------------------------------
"""

mapTitle = "=================================\nNeural Net Map\n================================="
backPropTitle = "=================================\nBack Propagation\n================================="
propLoopTitle = "---------------------------------\nBack Propagation (Loop: %d)\n---------------------------------"




dStruct = {
	'input' : [],
	'max_iterations' : 0,
	'error_threshhold' : 0,
	'n_inputs' : 0,
	'n_outputs' : 0,
	'n_hiddenLayers' : 0,
	'n_neuronsPerHidden' : 0,
	'rateOfLearning' : 0,
	'target' : 0
}

class indent():
	indentorUnit = ''
	outputString = ''

	def __init__(self, unit):
		self.indentorUnit = unit
		self.outputString = ''

	def increment(self):
		self.outputString = self.outputString + self.indentorUnit
		return self.outputString

	def currentString(self):
		return self.outputString

	def decrement(self):
		self.outputString = self.outputString[0:(len(self.outputString) - len(self.indentorUnit))]
		return self.outputString

def hasKey(string, dictionary):
	if string in dictionary.keys():
		return True
	return False

def main():
	if (not len(sys.argv) == 2):
		raise ValueError('Main.py: wrong number of command line arguments. Asks for 1, %d given.' % (len(sys.argv) - 1))
	datas = getDataFromFile(sys.argv[1])
	for i in datas:
		if hasKey(i[0], dStruct):
			dStruct[i[0]] = eval(i[1])
	print dStruct
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['n_neuronsPerHidden'])

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
	return

if __name__ == "__main__": main()

