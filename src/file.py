"""
  file.py
  by David Weinman
  5/1/13, 11:25p
"""

"""
This file is licensed under the MIT License, see LICENSE for details.
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
of the form 'dataLabel = dataValue'
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

"""
takes a list containing a key and a value to save to a given filename
(data), and a filename (fileName). if the data already exists in the
file (assuming the form dataLabel = dataValue) then it will replace it, 
if not it appends it to the file in the form dataLabel = dataValue.
"""
def saveDataToFile(data, fileName):
	file = open(os.getcwd() + '/' + fileName)
	count = 0
	if hasSubString(data[0], fileName):
		for i in file:
			if i.count(data[0]) > 0:
				file.close()
				file = open(os.getcwd() + '/' + fileName)
				lines = list(file)
				lines[count] = lines[count][0:(-1 * len(lines[count].split(' = ')[1]))] + ('%d\n' % data[1])
				file.close()
				os.remove(os.getcwd() + '/' + fileName)
				file = open(os.getcwd() + '/' + fileName, "w")
				for j in lines:
					file.write(j)
				file.close()
				break
			count += 1
	else:
		file.close()
		file = open(os.getcwd() + '/' + fileName, "a")
		file.write(('%s = ' + str(data[1]) + '\n') % data[0])
		file.close()
	return

"""
takes a string to search for and a file to search in. returns true
if the file has the substring and false if not
"""
def hasSubString(string, fileName):
	file = open(os.getcwd() + '/' + fileName)
	for i in file:
		if i.count(string) > 0:
			return True
	return False

