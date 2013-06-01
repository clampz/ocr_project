"""
  neuralNet.py
  by David Weinman
  4/21/13, 5:30p

"""

import sys
import random
import math
import propagate
from main import *

class neuron():
	n_inputs = 0
	l_weights = []

	def __init__(self, numberOfInputs):
		self.l_weights = []
		self.n_inputs = numberOfInputs
		for i in range(0,(numberOfInputs)): #for each input + threshhold
			self.l_weights.append(random.uniform(-1,1))
		self.l_weights.append(0) # set threshold to zero.

	def toString(self):
		return str(self.l_weights[0:-1]) + ', threshhold: ' + str(self.l_weights[-1])

	#
	def putWeights(self, weights):
		for i in range(0, len(weights)):
			self.l_weights[i] = weights[i]

class neuralNetLayer():
	n_neurons = 0
	neurons = []

	def __init__(self, numNeurons, numInputsPerNeuron):
		self.neurons = []
		self.n_neurons = numNeurons
		for i in range(0, numNeurons):
			#print('neuralNetLayer -> length of self.neurons: %d' % len(self.neurons))
			#print("neural net layer makes a neuron -> %d" % i)
			self.neurons.append(neuron(numInputsPerNeuron))

	def printLayer(self, indentor):
		for i in range(0, len(self.neurons)):
			print(indentor.currentString() + ('neuron %d : ' % i) + self.neurons[i].toString())

	def getWeights(self):
		weights = []
		for i in range(0, self.n_neurons):
			i_weights = []
			for j in range(0, len(self.neurons[i].l_weights)):
				i_weights.append(self.neurons[i].l_weights[j])
			weights.append(i_weights)
		return weights

######### layers, neurons vs l_weights
######### numberOfNeuronsArray
class neuralNet():
	n_inputs = 0
	n_outputs = 0
	n_hiddenLayers = 0
	neurons
	layers = []

	def __init__(self, numInputs, numOutputs, numHidden, neuronsInHiddenArray):
		self.layers = []
		self.n_inputs = numInputs
		self.n_outputs = numOutputs
		self.n_hiddenLayers = numHidden
		self.n_neuronsPerHiddenLyr = 
		#print('making input layer with %d neurons and %d inputs to the neurons' % (numInputs, numInputs))
		self.layers.append(neuralNetLayer(numInputs, numInputs))# make input layer
		for i in range(0, self.n_hiddenLayers):
			#print('making hidden layer with %d neurons and %d inputs to the neurons' % (numNeuronsPerHidden, numNeuronsPerHidden))
			self.layers.append(neuralNetLayer(numNeuronsPerHidden, numNeuronsPerHidden))# make hidden layers
		if numHidden > 0: # if you have hidden neurons, output will connect to them
			#print('making output layer with %d neurons and %d inputs to the neurons' % (numOutputs, numNeuronsPerHidden))
			self.layers.append(neuralNetLayer(numOutputs, numNeuronsPerHidden))
		else:
			#print('making output layer with %d neurons and %d inputs to the neurons' % (numOutputs, numInputs))
			self.layers.append(neuralNetLayer(numOutputs, numInputs))# make output layer connect to input layer

	def printNN(self):
		indentor = indent('  ')
		print(indentor.currentString() + 'neural net printout:')
		for i in range(0, len(self.layers)):
			print('layer %d' % i)
			indentor.increment()
			self.layers[i].printLayer(indentor)
			indentor.decrement()

	#returns a list of the weights in the net
	def getWeights(self):
		weights = []
		for i in range(0, self.n_hiddenLayers + 1): #+ 1 because output layer
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
			for j in range(0, self.layers[i].n_neurons):
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
					outputs.append(propagate.y(outputPriorLayer, self.layers[i].neurons[j]))
				else:
					outputs.append(propagate.y(inputs, self.layers[i].neurons[j]))
			outputPriorLayer = outputs
		return outputs[0:len(self.layers[-1].neurons)]



