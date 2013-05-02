"""
  main.py
  by David Weinman
  4/23/13, 3:25a
"""

from neuralNet import *
from propagate import *
from fileReader import *

"""

"""

dStruct = {
	'input' : []
	'max_iterations' : 0
	'error_threshhold' : 0
	'n_inputs' : 0
	'n_outputs' : 0
	'n_hiddenLayers' : 0
	'n_neuronsPerHidden' : 0
	'rateOfLearning' : 0
	'target' : 0
}


def hasKey(string, dictionary):
	if string in dictionary.keys():
		return True
	return False

def main():
	# i want to print some rad prompt here..
	filename = raw_input('enter a filename: ')
	datas = getDataFromFile(filename)
	for i in datas:
		if hasKey(i[0], dStruct):
			dStruct[i[0]] = i[1]
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['n_neuronsPerHidden'])
	backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'])
	return

if __name__ == "__main__": main()

