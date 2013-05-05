"""
  propagate.py
  by David Weinman
  4/26/13, 9:10p
"""
from neuralNet import *


"""
backProp takes a neural network (inputNN), a set of input training values (input),
a number of maximum allowed iterations (max_iterations), and a threshold for the
calculated error values, this last value is used as a way to tell when the network
has been sufficiently trained. back propagation is an algorithm for training a
neural network.
"""

def backProp(inputNN, input, targets, max_iterations, error_threshhold, learningRate):
	n_iterations = 0 # counter for the number of propagation loops
	netError = float(error_threshhold + 1.0)
	#print('max_iterations: %d, error_threshhold: %f, netError: %f, n_iterations: %d' % (max_iterations, error_threshhold, netError, n_iterations))
	#print('eval of while loop: %s' % (n_iterations < max_iterations and netError > error_threshhold))
	while ((n_iterations < max_iterations) and (netError > error_threshhold)):
		print('1backProp iteration = %d, netError = %f' % (n_iterations, netError))
		countPatterns = 0
		for i in input:
			outputCurrentPattern = inputNN.update(i) # present the pattern to the network
			outputLayerError = errorGradientOutputLayer(sum(outputCurrentPattern), targets[countPatterns]) #calc the error signal, assumes that output layer has only 1 node.
			newWeights = [] # to collect new weights for updating the neurons
			inputsForWeightChangeLoop = i # this is actually to collect outputs for computing the weight change in hidden layers, which are then used as inputs
			#print('2backProp iteration = %d, netError = %f, inputsForWeightChangeLoop:' % (n_iterations, netError))
			#print(inputsForWeightChangeLoop)
			counter = 0 # used for a condition to compute the error value in the hidden layer above the output layer.
			layersFromOut = list(range(0, inputNN.n_hiddenLayers + 1)) # this is in order to get the reverse of a list to do a backwards propagation,  + 1 for input layer
			layersFromOut.reverse() # reverses the list
			error2DArray = [] # this collects error values for use in the change of the weights
			for j in layersFromOut: # for every layer, starting with the hidden layer closest to output.
				for k in range(0, inputNN.layers[j].n_neurons): # for every neuron in the layer
					if counter != 0: # if the neuron isn't in the hidden layer above the output
						error2DArray.append(errorGradientHiddenLayer(k, j, inputNN, error2DArray[j + 1]))  # compute the error gradient for the neuron
					else:
						error2DArray.append(errorGradientHiddenLayer(k, j, inputNN, [outputLayerError])) # '' same but for the hidden layer above the output layer
				counter += 1
			for j in range(0, inputNN.n_hiddenLayers + 2): # for every layer, + 2 in range for output and input layers.
				for k in range(0, inputNN.layers[j].n_neurons): # for every neuron in the layer
					newWeights = []
					for h in range(0, inputNN.layers[j].neurons[k].n_inputs): #for every weight in the neuron
#deltaWeight(float oldWeight, float learningRate, list[float] inputsToNeuron, list[float] errorValues, float derivitiveOfActivationFn)
						newWeights.append(deltaWeight(inputNN.layers[j].neurons[k].l_weights[h], learningRate, inputsForWeightChangeLoop[h], error2DArray[j], derivActivation(inputsForWeightChangeLoop, inputNN.layers[j].neurons[k]))) # get the change in weight
					inputNN.layers[j].neurons[k].putWeights(newWeights) #update the weights
				#print('3backProp iteration = %d, netError = %f, inputsForWeightChangeLoop:' % (n_iterations, netError))
				print(inputsForWeightChangeLoop)
				oldInputsWeightChange = inputsForWeightChangeLoop # this is used to calculate the new inputs for the change in weight
				inputsForWeightChangeLoop = [] # clear it to re-populate
				for k in range(0, inputNN.layers[j].n_neurons): # for every neuron in the layer
					#print('4backProp iteration = %d, netError = %f, inputsForWeightChangeLoop:' % (n_iterations, netError))
					#print(inputsForWeightChangeLoop)
					#print('5backProp, oldInputsWeightChange:')
					#print(oldInputsWeightChange)
					#print('6backProp, inputNN.layers[j].neurons[k]:')
					#print(inputNN.layers[j].neurons[k])
					#print('8backProp, y(stuff):')
					#print(float(math.e**activation(oldInputsWeightChange, inputNN.layers[j].neurons[k]) - math.e**((-1) * activation(oldInputsWeightChange, inputNN.layers[j].neurons[k])))/float(math.e**activation(oldInputsWeightChange, inputNN.layers[j].neurons[k]) + math.e**((-1) * activation(oldInputsWeightChange, inputNN.layers[j].neurons[k]))))
					#print('9backProp, y(stuff):')
					#print(sigmoid(activation(oldInputsWeightChange, inputNN.layers[j].neurons[k])))
					#print('7backProp, y(stuff):')
					#print(y(oldInputsWeightChange, inputNN.layers[j].neurons[k]))
					inputsForWeightChangeLoop.append(float(y(oldInputsWeightChange, inputNN.layers[j].neurons[k])))
					#inputsForWeightChangeLoop.append(y(oldInputsWeightChange, inputNN.layers[j].neurons[k])) # calculate the new inputs
			n_iterations += 1
			errorVal = 0# sum unit for the net error
			for j in range(0, len(input)): # for every pattern in the training set
				for k in range(0, inputNN.layers[-1].n_neurons): # for every output to the net
					errorVal += errorSignal(targets[k], outputCurrentPattern[k])
			netError = .5  *  errorVal #calc the error fn for the net?
			counter += 1
			print('2backProp iteration = %d, netError = %f' % (n_iterations, netError))
		#
	#print('propagate finished with %d iterations and %f net error' % (n_iterations, netError))
	return

"""
errorSignal takes ...
returns the error for some given neuron and input
"""
def errorSignal(target, activation):
	return (target - activation)**2
	

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
	return float(math.e**activation - math.e**((-1) * activation))/float(math.e**activation + math.e**((-1) * activation))

        #return 1/float(1 + (math.e**((-activation) / 1.0))) # where curve shape or 'p' is set to 1.0

"""
sigmoid f'ns derivative.
"""
def derivSigmoid(activation):
	return sigmoid(activation) * (1 - sigmoid(activation))

"""
errorGradientOutputLayer takes an output of some neuron, n (outputN) and a target
value for the same neuron, n (targetN) and produces the basic error gradient
f'n for some output neuron. [this f'n is specific to the output layer of neurons]
"""
def errorGradientOutputLayer(outputN, targetN):
	return outputN * (1 - outputN) * (targetN - outputN)

"""
errorGradientHiddenLayer takes a neuron index for some hidden neuron, n (neuronIndex), 
a layer index for this neuron(layerIndex), an error value for the prior layer 
(errorValue), and a neuralNet to which the hiddenN belongs (neuralNet) and returns
the basic error gradient f'n for some hidden neuron.
"""
def errorGradientHiddenLayer(neuronIndex, layerIndex, neuralNet, errorValue):
	weights = neuralNet.layers[layerIndex + 1].getWeights()
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
	activationValue += (-1) * n.l_weights[-1] # threshhold?
	return activationValue

"""
activation f'ns derivative
"""
def derivActivation(p, n):
	return activation(p, n) * sigmoid(activation(p, n)) * (1 - sigmoid(activation(p, n)))

"""
deltaThreshhold takes a target value for some pattern (targetP), an output value 
for some pattern; for some node (outputP) and returns the change in threshhold value
for that input on that node.
"""
def deltaThreshhold(targetP, outputP):
	return (-1) * (targetP - outputP)

"""
deltaWeight takes ...
returns the change in weight for the given oldWeight
"""
def deltaWeight(oldWeight, learningRate,  x, errorValue, derivAct):
	return oldWeight + (learningRate * errorValue * derivAct * x)
#def deltaWeight(targetP, outputP, inputPI):
#	return (targetP - outputP) * inputPI

"""
sum takes a list of numbers and returns the sum of a list of numbers.
"""
def sum(lst):
	output = 0
	for i in range(0, len(lst)):
		output += lst[i]
	return output


"""
backprop algorithm:
while (number of iterations < max_iterations && error_fn > error_threshhold) {

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

""" OLD CODE FOLLOWS..

                        #for j in range(0, (inputNN.n_hiddenLayers + 1)): # for every layer in the network; range 2nd param -> hidden layers + 1 for input layer
                        #       for k in range(0, inputNN.layers[j].n_neurons): # for every neuron in the layer
                        #               weightSumK = sum(inputNN.layers[j].neurons[k].l_weights) #calc the weight sum of the inputs to the node
                        #               activationK = activation(inputToNeuron, inputNN.layers[j].neurons[k]) #calc the activation for the node


"""

