"""
  fileReader.py
  by David Weinman
  5/1/13, 11:25p
"""

"""
"""

import os
from neuralNet import *

"""
takes a neural net object (inputNN) and a file name (filename)
and writes a 2D list containing the weights and thresholds in
the neural net to a new line at the end of the file.
"""
def saveNeuralNet(inputNN, filename):
	file = open(os.getcwd() + '/' + filename, "a")
	file.write(str(inputNN.getWeights()))

"""
getDataFromFile takes a file name (fileName) and returns a list
of the fields and their respective values split at equals
signs. this f'n assumes that every line in the fileName is
of the form 'data = value'
"""
def getDataFromFile(fileName):
	file = open(os.getcwd() + '/params/' + fileName)
	linesWithEquals = []
	linesOutputData = []
	for i in file:
		linesWithEquals.append(i.split('\n'))
	for i in linesWithEquals:
		linesOutputData.append(i[0].split(' = '))
	return linesOutputData


