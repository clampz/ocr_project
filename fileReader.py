"""
  fileReader.py
  by David Weinman
  5/1/13, 11:25p
"""

"""
"""

import os

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


