"""
  propagate.py
  by David Weinman
  4/26/13, 9:10p
"""

import os
import datetime
import numpy as np
from neuralNet import *
from pylab import xlabel, ylabel, show, plot, title, grid, savefig
from decimal import Decimal, getcontext
from copy import deepcopy as deepcopy
from random import randint as randint

# constants for printing
mapTitle = "=================================\nNeural Net Map\n================================="
backPropTitle = "=================================\nBack Propagation\n================================="
propLoopTitle = "---------------------------------\nBack Propagation (Loop: %d)\n---------------------------------"

# these are arrays to log neural network error values to visualize a graph while training
errorArray = []
iterations = []

"""
backProp takes a neural network (inputNN), a set of input training values (input),
a number of maximum allowed iterations (max_iterations), a threshold for the
calculated error values (error_threshold) in order to tell when the network has
been sufficiently trained, and a constant learning rate for weight and threshold updates
(learningRate). backProp returns a boolean representation of how it finished training, 
True if it finished by error_threshold and False if by max_iterations. back propagation 
is a supervised training algorithm for training a neural network.
"""
def backProp(inputNN, trainingSet, targets, max_iterations, error_threshold, learningRate):
	n_iterations = 0 # counter for the number of propagation loops
	netError = float(error_threshold + 0.1)

## -------------- foward propagate inputs through net and populate a list of outputs for training
	outputs = [[]] * len(targets)
	for i in range(0, len(targets)):
		outputs[i] = inputNN.update(trainingSet[i])

## -------------- get the current time, make a directory labeled with it to put error graphs in and make it the cwd
	now = datetime.datetime.now()
	print('now: ' + str(now))
	originalDir = os.getcwd()
	os.mkdir('errorGraphs_' + str(now))
	os.chdir('errorGraphs_' + str(now))

	print(backPropTitle) # prints out prompt to label the beginning of training

	while ((n_iterations < max_iterations) and (netError > error_threshold)):

		print(propLoopTitle % n_iterations) # see global constants. prints which loop is training
		countPatterns = 0 # counter for the number of patterns into input the loop is

		input = randLst(zip(trainingSet, targets)) # makes a randomized list of tuples with the training inputs and their respective targets
		for i in input: #for every pattern in the training set 

## -------------- foward propagate input through net
			outputCurrentPattern = inputNN.update(i[0])

## -------------- error calculation -> setup arrays to propagate error backwards
			outputLayerError = [] # create empty array for the error of the nodes in output layer
			for j in range(0, inputNN.l_layers[-1].n_neurons): # for every node in the output layer
				#outputLayerError.append(errorGradientOutputLayer(outputCurrentPattern[j], input[countPatterns][1])) #calc the error in the output layer
				outputLayerError.append(errorGradientOutputLayer(outputCurrentPattern[j], input[countPatterns][1][j])) #calc the error in the output layer
			newWeights = [] # to collect new weights for updating the neurons
			inputsForWeightChangeLoop = i[0] # this is actually to collect outputs for computing the weight change in hidden layers, which are then used as inputs

## -------------- error calculation -> calculate and store for weight updates
			counter = 0 # used for a condition to compute the error value in the hidden layer above the output layer.
			layersFromOut = list(range(1, inputNN.n_hiddenLayers + 2)) # this is in order to get the reverse of a list to do a backwards propagation,  + 1 for output layer
			layersFromOut.reverse() # reverses the list
			error2DArray = [] # this collects error values for use in the change of the weights
			for j in layersFromOut: # for every layer, starting with the output
				while (len(error2DArray) < (j + 1)): # keep the array big enough to write like a backprop
					error2DArray.append([])
				if (j != layersFromOut[0]): # if we're not dealing with the output layer
					for k in range(0, inputNN.l_layers[j].n_neurons): # for every neuron in the layer
						if counter != 0: # if the neuron isn't in the hidden layer above the output
							error2DArray[j].append(errorGradientHiddenLayer(k, j, inputNN, error2DArray[j + 1]))  # compute the error gradient for the neuron
						else:
							error2DArray[j].append(errorGradientHiddenLayer(k, j, inputNN, outputLayerError)) # '' same but for the hidden layer above the output layer
					counter += 1
				else: # deal with the output layer
					error2DArray[j] = outputLayerError

## -------------- weight / threshold update
			for j in range(1, inputNN.n_hiddenLayers + 1): # for every hidden layer, + 1 in range for output layer. (the + 2 was weird, but it made it so the output layer was always updated)
				for k in range(0, inputNN.l_layers[j].n_neurons): # for every neuron in the layer
					newWeights = []
					for h in range(0, inputNN.l_layers[j].l_neurons[k].n_inputs): #for every weight in the neuron

								 # def deltaWeight(oldWeight, learningRate,  x, errorValue, derivAct):
						newWeights.append(deltaWeight(inputNN.l_layers[j].l_neurons[k].l_weights[h], learningRate, inputsForWeightChangeLoop[h], error2DArray[j][k], derivActivation(inputsForWeightChangeLoop, inputNN.l_layers[j].l_neurons[k])))
                                                # ^^^^ get the change in weight

					inputNN.l_layers[j].l_neurons[k].putWeights(newWeights) #update the weights

					inputNN.l_layers[j].l_neurons[k].l_weights[-1] = deltaThreshold(inputNN.l_layers[j].l_neurons[k], error2DArray[j][k], learningRate) # update the threshold

				oldInputsWeightChange = inputsForWeightChangeLoop # this var is used to calculate the new inputs for the change in weight
				inputsForWeightChangeLoop = [] # clear it to re-populate
				for k in range(0, inputNN.l_layers[j].n_neurons): # for every neuron in the layer
					inputsForWeightChangeLoop.append(float(y(oldInputsWeightChange, inputNN.l_layers[j].l_neurons[k]))) # collect the outputs to use for input to the next layer
			outputs[n_iterations % len(input)] = inputNN.update(i[0])

## -------------- network total error calculation and visualization
		n_iterations += 1
		errorVal = float(0) # sum unit for the net error
		for j in range(0, len(targets)): # for every pattern in the trainingset
			for h in range(0, inputNN.l_layers[-1].n_neurons): # for every output to the net
				errorVal += errorSignal(targets[j][h], outputs[j][h])
		netError = .5 * errorVal #calc the error fn for the net?
		errorArray.append(netError)
		iterations.append(n_iterations)
		plot(iterations, errorArray, linewidth=1.0) # plot(xArray, yArray, ...) from pylab lib
		xlabel('iterations')
		ylabel('error')
		title('error while training')
		grid(True)
		savefig('errorGraph' + str(n_iterations) + '.png')
		#im = Image.open('errorGraph' + str(n_iterations) + '.png') #### it would be so cool to display the error (GUI) instead of just saving it to files
		#im.show()                                                  #### I need to learn to use Popen in subprocess

## -------------- print stuff
		print(mapTitle)
		inputNN.printNN()

	print('propagate finished with %d iterations and %f net error' % (n_iterations, netError))
	os.chdir('..') # go to parent dir for calling f'ns purposes
	return (netError < error_threshold)
"""
backProp
"""

"""
errorSignal takes a target value for some given neuron (target)
and the output value for that given neuron (activation) and
returns the error for some given neuron and input
"""
def errorSignal(target, activation):
	return float((target - activation)**2)

"""
y takes a set of patterns or inputs (p), and a neuron (n) and returns the 
output for the specified node in the neural net. [keep in mind that the
input of some neuron is really in terms of the layer above it.]
"""
def y(p, n):
	if (len(p) != n.n_inputs): # if the node has a different number of inputs than specified in params, throw error.
		raise ValueError('wrong number of inputs: y(p, n) in propagate.')
	return sigmoid(activation(p, n))

"""
sigmoid takes an activation value (activation) and calculates the sigmoid 
function on the activation value. [here I use the tanh function]
"""
def sigmoid(activation):
	#return np.longfloat(math.e**activation - math.e**((-1) * activation)/np.longfloat(math.e**activation + math.e**((-1) * activation)))
    return 1/float(1 + (math.e**((-activation) / 1.0))) # where curve shape or 'p' is set to 1.0

"""
sigmoid f'ns derivative. takes an activation value (activation) and returns the 
derivative of the sigmoid function.
"""
def derivSigmoid(activation):
	return sigmoid(activation) * (1 - sigmoid(activation))

"""
errorGradientOutputLayer takes an output of some neuron, n (outputN) and a target
value for the same neuron, n (targetN) and produces the basic error gradient
f'n for some output neuron. [this f'n is specific to the output layer of neurons]
"""
def errorGradientOutputLayer(outputN, targetN):
#	print('errorGradientOutputLayer(outputN value: %s, targetN value: %s)' % (str(outputN), str(targetN)))
	return outputN * (1 - outputN) * (targetN - outputN)

"""
errorGradientHiddenLayer takes a neuron index for some hidden neuron, n (neuronIndex), 
a layer index for this neuron(layerIndex), an error value for the prior layer 
(errorValue), and a neuralNet to which the hiddenN belongs (neuralNet) and returns
the basic error gradient f'n for some hidden neuron.
"""
def errorGradientHiddenLayer(neuronIndex, layerIndex, neuralNet, errorValue):
	weights = neuralNet.l_layers[layerIndex + 1].getWeights()
	sumOut = 0
	for i in range(0, len(weights)): # for every neuron in the layer below
		sumOut += errorValue[i] * weights[i][neuronIndex]
	return sumOut

"""
activation takes a neuron (n) and a set of patterns or inputs (p) and returns
the activation value of the neuron on that input pattern.
"""
def activation(p, n):
	activationValue = 0
	for i in range(0, len(p)):
		activationValue += p[i] * n.l_weights[i]
	activationValue += (-1) * n.l_weights[-1]
	return activationValue

"""
activation f'ns derivative. takes a neuron (n) and a set of patterns or inputs (p)
and returns the derivative of the activation function.
"""
def derivActivation(p, n):
	return activation(p, n) * sigmoid(activation(p, n)) * (1 - sigmoid(activation(p, n)))

"""
deltaThreshhold takes a neuron (neuron), error value for that neuron (error),
an alpha constant or learning rate (learningRate) and returns the change in threshold
for that neuron
"""
def deltaThreshold(neuron, error, learningRate):
	return neuron.l_weights[-1] - (error * learningRate)

"""
deltaWeight takes the current weight value for the given input and neuron (oldWeight),
a learning rate constant for the neural net (learningRate), the input to that branch for
that neuron (x), the error value for the neuron (errorValue), and the derivative of the
activation for that neuron (derivAct) and returns the change in weight for the given oldWeight
"""
def deltaWeight(oldWeight, learningRate,  x, errorValue, derivAct):
	#print('deltaWeight(oldWeight: %s, learningRate: %s,  x: %s, errorValue: %s, derivAct: %s)' % (oldWeight, learningRate,  x, errorValue, derivAct))
	return oldWeight + (learningRate * errorValue * derivAct * x)
#def deltaWeight(targetP, outputP, inputPI):
#	return (targetP - outputP) * inputPI

"""
randLst takes a list (lst) and returns a new list with the same contents but randomly
re-ordered.
"""
def randLst(lst):
	output = []
	inputLst = deepcopy(lst)
	for i in range(0, len(lst)):
		output.append(inputLst[random.randint(0, len(inputLst) - 1)])
		inputLst.remove(output[-1])
	return output

"""
sum takes a list of numbers and returns the sum of a list of numbers.
"""
def sum(lst):
	output = 0
	for i in range(0, len(lst)):
		output += lst[i]
	return output

""" PSEUDO

def backprop():
while (number of iterations < max_iterations && error_fn > error_threshold) {

        for every pattern in the training set {

                present the pattern to the network
                for each layer in the network {

                        for each node in the layer {

                                calculate the weight sum of the inputs to the node
                                calculate the activation for the node

                        }

                }
                for every node in the output layer {

                        calculate the error signal

                }
                for all hidden layers {

                        for every node in the layer {

                                calculate the node's signal error
                                update each node's weight in the network

                        }

                }
                calculate the error fn

        }

}


"""

""" COPYPASTA
#			print('inputs: %s' % i[0])
#			print('outputs: %s' % outputCurrentPattern)
#			for j in range(0, len(inputNN.l_layers)):
#				print('error for layer %d: %s' % (j, error2DArray[j]))

"""

