"""
  neuralNet.py
  by David Weinman
  4/21/13, 5:30p

"""

import sys
import random
import math

class neuron():
	n_inputs = 0
	l_weights = []

	def __init__(self, numberOfInputs):
		self.n_inputs = numberOfInputs
		for i in range(0,(numberOfInputs + 2)): #for each input + threshhold & buf for range
			self.l_weights.append(random.randint(-1,1))

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

	#return the set of activation values for the layer
	#def activationValues(self):
		

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
		if (numHidden > 0):
			self.layers.append(neuralNetLayer(numNeuronsPerHidden, numInputs))
			for i in range(0, self.n_hiddenLayers):
				self.layers.append(neuralNetLayer(numNeuronsPerHidden, numNeuronsPerHidden))
			self.layers.append(neuralNetLayer(numOutputs, numInputs))

# get weights?
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
				for k in range(0, self.layers[i].neurons[j].n_inputs + 1):
					counter += 1
					self.layers[i].neurons[j].l_weights[k] = weights[counter]

	#returns the number of weights in the net
	def getNumWeights(self):
		num = 0
		for i in range(0, self.n_hiddenLayers + 1):
			for j in range(0, self.layers[i].n_neurons + 1):
				for k in range(self.layers[i].neurons[j].n_inputs + 1):
					num += 1
		return num
		
	# given some inputs, returns the output of the net
"""	def update(self, inputs):
		outputs = []
		counter = 0
		if (len(inputs) != self.n_inputs):
			return outputs
		for i in range(0, self.n_hiddenLayers + 1):
			# my neural nets tutorial had some weird assignment here, whats with that?
			counter = 0
			outputs = []
			for j in range(0, self.layers[i].n_neurons + 1):
				netInput = 0
				numInputs = self.layers[i].neurons[j].n_inputs
				for k in range(0, numInputs + 1):# num inputs + buf for range
					netInput += self.layers[i].neurons[j].weights[numInputs - 1] * 	

"""


