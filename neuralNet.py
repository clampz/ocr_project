"""
  neuralNet.py
  by David Weinman
  4/21/13, 5:30p

"""

import sys
import random
import math
from propagate import *

class neuron():
	n_inputs = 0
	l_weights = []

	def __init__(self, numberOfInputs):
		self.n_inputs = numberOfInputs
		for i in range(0,(numberOfInputs + 2)): #for each input + threshhold & buf for range
			self.l_weights.append(random.randint(-1,1))

	# replace the weights in this neuron
	def putWeights(weights):
		for i in range(0, len(weights)):
			self.l_weights[i] = weights[i]

class neuralNetLayer():
	n_neurons = 0
	neurons = []

	def __init__(self, numNeurons, numInputsPerNeuron):
		self.n_neurons = numNeurons
		for i in range(0, numNeurons + 1):
			self.neurons.append(neuron(numInputsPerNeuron))

	def getWeights(self):
		weights = []
		for i in range(0, self.n_neurons + 1):
			i_weights = []
			for j in range(0, len(self.neurons[i].l_weights) + 1):
				i_weights.append(neurons[i].l_weights[j])
			weights.append(i_weights)
		return weights

class neuralNet():
	n_inputs = 0
	n_outputs = 0
	n_hiddenLayers = 0
	n_neuronsPerHiddenLyr = 0
	layers = []

	def __init__(self, numInputs, numOutputs, numHidden, numNeuronsPerHidden):
		self.n_inputs = numInputs
		self.n_outputs = numOutputs
		self.n_hiddenLayers = numHidden
		self.n_neuronsPerHiddenLyr = numNeuronsPerHidden
		if (numHidden > 0):# if user wants hidden layers
			self.layers.append(neuralNetLayer(numNeuronsPerHidden, numInputs))# make input layer
			for i in range(0, self.n_hiddenLayers):
				self.layers.append(neuralNetLayer(numNeuronsPerHidden, numNeuronsPerHidden))# make hidden layers
			self.layers.append(neuralNetLayer(numOutputs, numInputs))# make output layer
		else:
			self.layers.append(neuralNetLayer(numInputs, numInputs))# make input layer
			self.layers.append(neuralNetLayer(numOutputs, numInputs))# make output layer

	#returns a list of the weights in the net
	def getWeights(self):
		weights = []
		for i in range(0, self.n_hiddenLayers + 2): #+ 2 because range and [output layer?]
			for j in range(0, self.layers[i].n_neurons + 1):
				for k in range(0, self.layers[i].neurons[j].n_inputs + 1):
					weights.append(self.layers[i].neurons[j].l_weights[k])
		return weights

	#replaces the weights in the net with the given values
	def putWeights(self, weights):
		counter = 0
		for i in range(0, self.n_hiddenLayers + 1):
			for j in range(0, self.layers[i].n_neurons + 1):
				self.layers[i].neurons[j].putweights(weights[i][j])

	#returns the number of weights in the net
	def getNumWeights(self):
		num = 0
		for i in range(0, self.n_hiddenLayers + 1):
			for j in range(0, self.layers[i].n_neurons + 1):
				for k in range(self.layers[i].neurons[j].n_inputs + 1):
					num += 1
		return num
		
	# given some inputs, returns the output of the net
	def update(self, inputs):
		if (len(inputs) != self.n_inputs):
			raise ValueError('wrong number of inputs: update() in neuralNet.')
		for i in range(0, self.n_hiddenLayers + 1): # I need to do this for every hidden layer + input layer.
			outputs = []
			for j in range(0, self.layers[i].n_neurons):
				if i != 0:# if current layer is not input layer
					outputs.append(y(outputPriorLayer, self.layers[i].neurons[j]))
				else:
					outputs.append(y(inputs, self.layers[i].neurons[j]))
			outputPriorLayer = outputs
		if n_outputs == 1:
			return outputs[0]
		else:
			return outputs[0:n_outputs]



