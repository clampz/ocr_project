#!/usr/bin/python

"""
  main.py
  by David Weinman
  4/23/13, 3:25a
"""

import os
import sys
import datetime
from copy import deepcopy
from neuralNet import *
from indenter import indenter
from propagate import backProp
from file import saveDataToFile, getDataFromFile, loadNeuralNet, saveNeuralNet
from capture import getImageValues, decomposeParagraph

# these are string constants for neural net and training printouts
mapTitle = "=================================\nNeural Net Map\n================================="
backPropTitle = "=================================\nBack Propagation\n================================="
propLoopTitle = "---------------------------------\nBack Propagation (Loop: %d)\n---------------------------------"

# dictionary of params for the neural net training algorithm and image preprocessing
dStruct = {
	'input' : [],
	'max_iterations' : 0,
	'error_threshhold' : 0,
	'n_inputs' : 0,
	'n_outputs' : 0,
	'n_hiddenLayers' : 0,
	'neuronsInHidden' : [],
	'rateOfLearning' : 0,
	'target' : 0,
	'lineNumForNet' : 0,
	'imageSize' : (0, 0),
	'backgroundValue' : 0
}

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
takes a list (lst) and returns a list containing a single element;
the index of the max number in lst
"""
def imax(lst):
   m = max(lst)
   return [i for i, j in enumerate(lst) if j == m]

"""
takes a list containing the output of an ocr nn (lst) and returns the char
corresponding to the output
"""
def getClassMatch(lst):
   classes     = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?"]
   return classes[imax(lst)[0]]

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
	backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
	print('ok, so my neural net has %.20f rate of learning and %.20f error threshhold' % (dStruct['rateOfLearning'], dStruct['error_threshhold']))
	answer = eval(raw_input('do you want to run some input on the neural net? (enter True or False): '))
	while (answer):
		print("output:\n%s" % inputNeuralNet.update(dStruct['input'][eval(raw_input('which input do you want to use from the input patterns?(enter an int): '))]))
		print("\n\n\done ..\n\n")
		answer2 = eval(raw_input('\nok .. liek ... do you want to save your neural net? (enter True or False): '))
		if answer2:
			now = datetime.datetime.now()
			filename = raw_input('\nok .. liek ... what is your filename?: ')
			lineNo = saveNeuralNet(inputNeuralNet, filename)
			saveDataToFile(['lineNumForNet', lineNo], 'params/' + sys.argv[2])
			file = open(os.getcwd() + '/params/' + sys.argv[2], "a")
			file.write('\n\n' + str(now) + ' : ' + str(lineNo))
			file.close()
			print("\nthe line number it got saved at is: %d" % lineNo)
		answer = eval(raw_input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
	return

"""
takes a filename to get the neural net weights from (neuralNetFile)
and a line number to look for the weights at (neuralNetLineNum) and
writes out the recognized text from an image
"""
def runNeuralNetImageToText(neuralNetFile, neuralNetLineNum):
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])
	loadNeuralNet(inputNeuralNet, neuralNetFile, neuralNetLineNum)
	outputString = ''
	for i in dStruct['input']:
		outputString = outputString + getClassMatch(inputNeuralNet.update(i))
	return outputString

"""
sorts the options and calls appropriate functions respectively

python main.py -r params.dat neuralNets.dat
python main.py -t params.dat
python main.py -i -r params.dat neuralNets.dat
python main.py -i -t params.dat
python main.py --help
"""
def main():
	if (sys.argv[1] == "-r"):
		if (not len(sys.argv) == 4):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 3, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[2])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		runNeuralNet(sys.argv[3], dStruct['lineNumForNet'])
	elif (sys.argv[1] == "-t"):
		if (not len(sys.argv) == 3):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 2, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[2])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		trainNeuralNet()
	elif (sys.argv[1] == "-i" and sys.argv[2] == "-r"):
		if (not len(sys.argv) == 5):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 4, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[3])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		decomposeParagraph(dStruct['input'][0], (dStruct['imageSize'][0], dStruct['imageSize'][1]), dStruct['input'], dStruct['backgroundValue'])
		oldInput = deepcopy(dStruct['input'])
		oldInput.pop(0)
		dStruct['input'] = []
		for i in oldInput:
			dStruct['input'].append(getImageValues(i))
		#dStruct['target'] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?"]
		print 'output: ' + runNeuralNetImageToText(sys.argv[4], dStruct['lineNumForNet'])
	elif (sys.argv[1] == "-i" and sys.argv[2] == "-t"):
		if (not len(sys.argv) == 4):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 3, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[3])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		decomposeParagraph(dStruct['input'][0], (dStruct['imageSize'][0], dStruct['imageSize'][1]), dStruct['input'], dStruct['backgroundValue'])
		oldInput = deepcopy(dStruct['input'])
		oldInput.pop(0)
		dStruct['input'] = []
		for i in oldInput:
			dStruct['input'].append(getImageValues(i))
		inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])
		backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
                #filename = raw_input('\nok .. liek ... what is your filename?: ')
                lineNo = saveNeuralNet(inputNeuralNet, sys.argv[4])
                now = datetime.datetime.now()
                saveDataToFile(['lineNumForNet', lineNo], 'params/' + sys.argv[3])
                file = open(os.getcwd() + '/params/' + sys.argv[3], "a")
                file.write('\n\n' + str(now) + ' : ' + str(lineNo))
                file.close()
	elif (sys.argv[1] == "--help"):
		print("\nexamples:\npython main.py -r params.dat neuralNet.dat\npython main.py -t params.dat\npython main.py -i -r params.dat neuralNets.dat\npython main.py -i -t params.dat\npython main.py --help\n")
	else:
		raise ValueError('main.py: invalid option specified: %s' % sys.argv[1])
	return

if __name__ == "__main__": main()

"""PSEUDO

notConverged = False
while (notConverged == False)
	run the neural net with the given input 10 times unless the neural net converges
	if it converges:
		if output is "correct":
			notConverged = True
		else:
			if there is a history with more than one training session:
				find the minimum error in that training, and continue changing params slightly in that direction
			else:
				if the number of occurences of minimum errors is decreasing in the direction of params change:
					continue the params change in the direction of minimum errors
				else:
					prompt user for params change
	else:
		if there is a history with more than one training session:
			find the minimum error in that training, and continue changing params slightly in that direction
		else:
			ask the user to change params if there's no history to base a decision on
			if the number of occurences of minimum errors is decreasing in the direction of params change:
				continue the params change in the direction of minimum errors
			else:
				prompt user for params change

"""

""" SCRATCH

fp ; trainParams(float errorThreshold, net neuralNet, lst inputs, lst targets, float learningRate)

def trainParams():


fp ; 

def userPromptNewParams():

"""

""" JUNK

import os
import sys
import datetime
from copy import deepcopy
from neuralNet import *
from propagate import *
from capture import *
from file import *

def runNeuralNetImageToText(neuralNetFile, neuralNetLineNum):
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])
	loadNeuralNet(inputNeuralNet, neuralNetFile, neuralNetLineNum)
	outputString = ''
	for i in dStruct['input']:
		outputString = outputString + getClassMatch(inputNeuralNet.update(i))
	return outputString

def hasKey(string, dictionary):
        if string in dictionary.keys():
                return True
        return False

def imax(lst):
   m = max(lst)
   return [i for i, j in enumerate(lst) if j == m]

def getClassMatch(lst):
   classes     = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?"]
   return classes[imax(lst)[0]]

datas = getDataFromFile('params.dat')
for i in datas:
	if hasKey(i[0], dStruct):
		dStruct[i[0]] = eval(i[1])

decomposeParagraph(dStruct['input'][0], (dStruct['imageSize'][0], dStruct['imageSize'][1]), dStruct['input'], dStruct['backgroundValue'])
oldInput = deepcopy(dStruct['input'])
oldInput.pop(0)
dStruct['input'] = []
for i in oldInput:
	dStruct['input'].append(getImageValues(i))

inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])

dStruct['target'] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?"]

print 'output: ' + runNeuralNetImageToText('neuralNet.dat', dStruct['lineNumForNet'])



	elif (sys.argv[1] == "-i" and sys.argv[2] == "-t"):
		if (not len(sys.argv) == 4):
			raise ValueError('main.py: wrong number of command line arguments. Asks for 3, %d given.' % (len(sys.argv) - 1))
		datas = getDataFromFile(sys.argv[3])
		for i in datas:
			if hasKey(i[0], dStruct):
				dStruct[i[0]] = eval(i[1])
		decomposeParagraph(dStruct['input'][0], (dStruct['imageSize'][0], dStruct['imageSize'][1]), dStruct['input'], dStruct['backgroundValue'])
		oldInput = deepcopy(dStruct['input'])
		dStruct['input'] = []
		for i in oldInput:
			dStruct['input'].append(getImageValues(i))
		dStruct['input'].pop(0) #removes initial paragraph image file from input list
		inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['neuronsInHidden'])
		dStruct['target'] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?"]
		backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
                #filename = raw_input('\nok .. liek ... what is your filename?: ')
                lineNo = saveNeuralNet(inputNeuralNet, sys.argv[4])
                now = datetime.datetime.now()
                saveDataToFile(['lineNumForNet', lineNo], 'params/' + sys.argv[3])
                file = open(os.getcwd() + '/params/' + sys.argv[3], "a")
                file.write('\n\n' + str(now) + ' : ' + str(lineNo))
                file.close()

=================================
=================================
---------------------------------
---------------------------------

[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]


# I'm testing the neural nets with fixed weights to start off with right now, so the loop below fixes the weights.
	#for i in inputNeuralNet.layers[0].neurons:
	#	i.putWeights([.5, .5])

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
