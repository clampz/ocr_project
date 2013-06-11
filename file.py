"""
  fileReader.py
  by David Weinman
  5/1/13, 11:25p
"""

"""
"""

import os
from neuralNet import *
from ast import literal_eval

"""
takes a neural net object (inputNN) and a file name (filename)
and writes a 2D list containing the weights and thresholds in
the neural net to a new line at the end of the file. returns an
integer representing the line number at which the 2D array lies
"""
def saveNeuralNet(inputNN, filename):
	file = open(os.getcwd() + '/' + filename)
	lineNo = len(list(file))
	file.close()
	file = open(os.getcwd() + '/' + filename, "a")
	file.write(str(inputNN.getWeights()))
	file.close()
	return lineNo

"""
takes a neural net object (inputNN), a file name (filename),
a line number at which the weights array is (n_line) and
loads the weights into the neural net.
"""
def loadNeuralNet(inputNN, filename, n_line):
	file = open(os.getcwd() + '/' + filename)
## -------------- get a list of the text, evaluate the line with the weights and load them
	inputNN.putWeights(literal_eval(list(file)[n_line]))
	file.close()

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
	file.close()
	return linesOutputData


