"""
  neuralNet.py
  by David Weinman
  4/21/13, 5:30p

---
Contains the classes needed to model the weights
to a neural net.
"""

"""
This file is licensed under the MIT License, see LICENSE for details.
"""

import sys
import random
import math
import propagate
from indenter import indenter

"""
neuron object takes a number which specifies the number
of inputs to the neuron (numberOfInputs)
"""
class neuron():
	n_inputs = 0
	l_weights = []

	def __init__(self, numberOfInputs):
		self.l_weights = []
		self.n_inputs = numberOfInputs
		for i in range(0,(numberOfInputs)): #for each input + threshhold
			self.l_weights.append(random.uniform(-1,1))
		self.l_weights.append(0) # set threshold to zero.

	# takes no params and returns a string representation of the neurons weights and threshold
	def toString(self):
		return str(self.l_weights[0:-1]) + ', threshold: ' + str(self.l_weights[-1])

	# takes a list of floats representing the weights in the neuron (weights) puts it in l_weights
	def putWeights(self, weights):
		for i in range(0, len(weights)):
			self.l_weights[i] = weights[i]

"""
net layer object takes a number which specifies the number of
neurons in the layer (numNeurons), and a number which specifies
the number of inputs per neuron (numInputsPerNeuron)
"""
class neuralNetLayer():
	n_neurons = 0
	l_neurons = []

	def __init__(self, numNeurons, numInputsPerNeuron):
		self.l_neurons = []
		self.n_neurons = numNeurons
		for i in range(0, numNeurons):
			#print('neuralNetLayer -> length of self.l_neurons: %d' % len(self.l_neurons))
			#print("neural net layer makes a neuron -> %d" % i)
			self.l_neurons.append(neuron(numInputsPerNeuron))

	# takes an indentor object and prints a string representation of the layer
	def printLayer(self, indentor):
		for i in range(0, len(self.l_neurons)):
			print(indentor.currentString() + ('neuron %d : ' % i) + self.l_neurons[i].toString())

	# takes no params and returns a list of the weights in the layer
	def getWeights(self):
		weights = []
		for i in range(0, self.n_neurons):
			i_weights = []
			for j in range(0, len(self.l_neurons[i].l_weights)):
				i_weights.append(self.l_neurons[i].l_weights[j])
			weights.append(i_weights)
		return weights

"""
net object takes a number of inputs to the net (numInputs),
a number of outputs from the net (numOutputs), a number of
hidden layers (numHidden), and a list of numbers representing
the number of neurons in each hidden layer (neuronsInHiddenArray).
"""
class neuralNet():
	n_inputs = 0
	n_outputs = 0
	n_hiddenLayers = 0
	l_layers = []

	def __init__(self, numInputs, numOutputs, numHidden, neuronsInHiddenArray):
		self.l_layers = []
		self.n_inputs = numInputs
		self.n_outputs = numOutputs
		self.n_hiddenLayers = numHidden
		#print('making input layer with %d neurons and %d inputs to the neurons' % (numInputs, numInputs))
		self.l_layers.append(neuralNetLayer(numInputs, numInputs))# make input layer
		for i in range(0, self.n_hiddenLayers):
			#print('making hidden layer with %d neurons and %d inputs to the neurons' % (numNeuronsPerHidden, numNeuronsPerHidden))
			self.l_layers.append(neuralNetLayer(neuronsInHiddenArray[i], neuronsInHiddenArray[i - 1]))# make hidden layers
		if numHidden > 0: # if you have hidden neurons, output will connect to them
			#print('making output layer with %d neurons and %d inputs to the neurons' % (numOutputs, numNeuronsPerHidden))
			self.l_layers.append(neuralNetLayer(numOutputs, neuronsInHiddenArray[-1]))
		else:
			#print('making output layer with %d neurons and %d inputs to the neurons' % (numOutputs, numInputs))
			self.l_layers.append(neuralNetLayer(numOutputs, numInputs))# make output layer connect to input layer

	# takes no params and prints a string represenation of the net
	def printNN(self):
		indentor = indenter('  ')
		print(indentor.currentString() + 'neural net printout:')
		for i in range(0, len(self.l_layers)):
			print('layer %d' % i)
			indentor.increment()
			self.l_layers[i].printLayer(indentor)
			indentor.decrement()

	#takes no params returns a 2D list of the weights and thresholds in the net
	def getWeights(self):
		weights = []
		for i in range(0, len(self.l_layers)): #+ 1 because output layer
			weights.append([])
			for j in range(0, self.l_layers[i].n_neurons):
				weights[i].append(self.l_layers[i].l_neurons[j].l_weights)
		return weights

	#takes a list of weights (weights) and replaces the weights in the net with the given values
	def putWeights(self, weights):
		counter = 0
		for i in range(0, self.n_hiddenLayers + 2):
			for j in range(0, self.l_layers[i].n_neurons):
				self.l_layers[i].l_neurons[j].putWeights(weights[i][j])
		
	# takes a list of numbers which represent the inputs to the net (inputs), and returns the output of the net
	def update(self, inputs):
		if (len(inputs) != self.n_inputs):
			raise ValueError('wrong number of inputs: update() in neuralNet.')
		for i in range(0, self.n_hiddenLayers + 1): # I need to do this for every hidden layer + input layer.
			outputs = []
			for j in range(0, self.l_layers[i].n_neurons):
				if i != 0:# if current layer is not input layer
					outputs.append(propagate.y(outputPriorLayer, self.l_layers[i].l_neurons[j]))
				else:
					outputs.append(propagate.y(inputs, self.l_layers[i].l_neurons[j]))
			outputPriorLayer = outputs
		return outputs[0:len(self.l_layers[-1].l_neurons)]



