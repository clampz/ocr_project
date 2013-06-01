"""
  propagate.py
  by David Weinman
  4/26/13, 9:10p
"""

from neuralNet import *
from main import *
from decimal import *

getcontext().prec = 15

"""
backProp takes a neural network (inputNN), a set of input training values (input),
a number of maximum allowed iterations (max_iterations), and a threshold for the
calculated error values, this last value is used as a way to tell when the network
has been sufficiently trained. back propagation is an algorithm for training a
neural network.
"""
def backProp(inputNN, input, targets, max_iterations, error_threshhold, learningRate):
	n_iterations = 0 # counter for the number of propagation loops
	netError = float(error_threshhold + 0.1)
	outputs = [[0]] * len(targets)
	print(backPropTitle)
	while ((n_iterations < max_iterations) and (netError > error_threshhold)):
		print(propLoopTitle % n_iterations)
		print('1backProp iteration = %d, netError = %.20f' % (n_iterations, netError))
		countPatterns = 0
####### need to random choose from input instead of iterating.
		for i in input: #for every pattern in the training set 
			outputs[n_iterations % len(targets)] = outputCurrentPattern = inputNN.update(i) # present the pattern to the network
			outputLayerError = [] # create empty array for the error of the nodes in output layer
			for j in range(0, inputNN.l_layers[-1].n_neurons): # for every node in the output layer
				outputLayerError.append(errorGradientOutputLayer(outputCurrentPattern[j], targets[countPatterns])) #calc the error in the output layer
			newWeights = [] # to collect new weights for updating the neurons
			inputsForWeightChangeLoop = i # this is actually to collect outputs for computing the weight change in hidden layers, which are then used as inputs
			counter = 0 # used for a condition to compute the error value in the hidden layer above the output layer.
			layersFromOut = list(range(0, inputNN.n_hiddenLayers + 2)) # this is in order to get the reverse of a list to do a backwards propagation,  + 2 for input & output layers
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
			for j in range(0, inputNN.n_hiddenLayers + 2): # for every layer, + 2 in range for output and input layers.
				for k in range(0, inputNN.l_layers[j].n_neurons): # for every neuron in the layer
					newWeights = []
					for h in range(0, inputNN.l_layers[j].l_neurons[k].n_inputs): #for every weight in the neuron
#deltaWeight(float oldWeight, float learningRate, list[float] inputsToNeuron, list[float] errorValues, float derivitiveOfActivationFn) INDEX ERROR ON LINE 46.
						newWeights.append(deltaWeight(inputNN.l_layers[j].l_neurons[k].l_weights[h], learningRate, inputsForWeightChangeLoop[h], error2DArray[j][k], derivActivation(inputsForWeightChangeLoop, inputNN.l_layers[j].l_neurons[k]))) # get the change in weight
					inputNN.l_layers[j].l_neurons[k].putWeights(newWeights) #update the weights
# how is error2DArray arranged? 
#def deltaThreshhold(neuron, error, learningRate):
#COMMENTED OUT LINE BELOW -- KEEPING THRESHOLD CONSTANT
					inputNN.l_layers[j].l_neurons[k].l_weights[-1] = deltaThreshold(inputNN.l_layers[j].l_neurons[k], error2DArray[j][k], learningRate) #deltaThreshold() # update the threshold
				oldInputsWeightChange = inputsForWeightChangeLoop # this is used to calculate the new inputs for the change in weight
				inputsForWeightChangeLoop = [] # clear it to re-populate
				for k in range(0, inputNN.l_layers[j].n_neurons): # for every neuron in the layer
					inputsForWeightChangeLoop.append(float(y(oldInputsWeightChange, inputNN.l_layers[j].l_neurons[k])))
			print('inputs: %s' % i)
			print('outputs: %s' % outputCurrentPattern)
			for j in range(0, len(inputNN.l_layers)):
				print('error for layer %d: %s' % (j, error2DArray[j]))
		n_iterations += 1
		errorVal = float(0) # sum unit for the net error
		for j in range(0, len(input)): # for every pattern in the trainingset
			for h in range(0, inputNN.l_layers[-1].n_neurons): # for every output to the net
				errorVal += float(errorSignal(targets[j], outputs[j][h]))
		netError = .5  *  errorVal #calc the error fn for the net?
		print(mapTitle)
		inputNN.printNN()
		print('2backProp iteration = %d, netError = %.20f' % (n_iterations - 1, netError))
		#
	#print('propagate finished with %d iterations and %f net error' % (n_iterations, netError))
	return

"""
errorSignal takes a target value for some given neuron (target)
and the output value for that given neuron (activation) and
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
	return float(Decimal(math.e**activation - math.e**((-1) * activation))/Decimal(math.e**activation + math.e**((-1) * activation)))

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
	activationValue += (-1) * n.l_weights[-1] # threshhold?
	return activationValue

"""
activation f'ns derivative
"""
def derivActivation(p, n):
	return activation(p, n) * sigmoid(activation(p, n)) * (1 - sigmoid(activation(p, n)))

""" UPDATE THE DESCRIPTION
deltaThreshhold takes a target value for some pattern (targetP), an output value 
for some pattern; for some node (outputP) and returns the change in threshhold value
for that input on that node.
"""
def deltaThreshold(neuron, error, learningRate):
	return neuron.l_weights[-1] - (error * learningRate)

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


