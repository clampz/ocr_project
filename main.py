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


def hasKey(string, dictionary):
	if string in dictionary.keys():
		return True
	return False

def main():
	# i want to print some rad prompt here..
	filename = input('enter a filename: ')
	datas = getDataFromFile(filename)
	for i in datas:
		if hasKey(i[0], dStruct):
			dStruct[i[0]] = eval(i[1])
	inputNeuralNet = neuralNet(dStruct['n_inputs'], dStruct['n_outputs'], dStruct['n_hiddenLayers'], dStruct['n_neuronsPerHidden'])
	backProp(inputNeuralNet, dStruct['input'], dStruct['target'], dStruct['max_iterations'], dStruct['error_threshhold'], dStruct['rateOfLearning'])
	answer = eval(input('do you want to run some input on the neural net? (enter True or False): '))
	while (answer):
		print("output:\n")
		print(inputNeuralNet.update(eval(input('ok .. so liek what\'s the input? (enter in the right form):'))))
		print("\n\n\done ..\n\n")
		answer = eval(input('\nok .. liek  ... do you want to run some more input on the neural net? (enter True or False): '))
	return

if __name__ == "__main__": main()

