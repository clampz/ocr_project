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
	priorLayerErrors = []
	for i in trainingSet:
		y = inputNN.update(input) # present the pattern to the network
		for j in range(0, (inputNN.n_hiddenLayers + 1)): # for every layer in the network; range 2nd param -> hidden layers + 1 for input layer
			for k in range(0, inputNN.layers[j].n_neurons): # for every neuron in the layer
				weightSumK = sum(inputNN.layers[j].neurons[k].l_weights) #calc the weight sum of the inputs to the node
				activationK = activation(inputToNeuron, inputNN.layers[j].neurons[k]) #calc the activation for the node
		priorLayerErrors.append(errorGradientOutputLayer(inputNN.layers[-1].neurons[0], targets[0])) #calc the error signal, assumes that output layer has only 1 node.
		counter = 0
		layersFromOut = range(0, n_hiddenLayers + 1) # + 1 for input layer
		layersFromOut.reverse()
		layersFromOut.pop(0) # remove the output layer
		for j in layersFromOut:# for every layer in the network
			jLayerErrors = []
			jLayerOutputK = []
			for k in range(0, inputNN.layers[j].n_neurons):# for every neuron in the layer
				jLayerOutputK.append(y())
				if counter != n_hiddenLayers: # if the layer isn't the input layer
					jLayerErrors.append(errorGradientHiddenLayer(inputNN.layers[j].neurons[k], j, inputNN, priorLayerErrors[k]))#calculate the error gradient for that neuron
					for h in range(0, inputNN.layers[j].neurons[k].n_inputs): #update each input's weight in the neuron
						deltaWeight(inputNN.layers[j].neurons[k].l_weights[h], learningRate,  priorLayerOutput[h], priorLayerErrors[k], derivActivation("""unknown inputs  so far"""))
				else: # then the layer is the input layer
					jLayerErrors.append(errorGradientHiddenLayer(inputNN.layers[j].neurons[k], j, inputNN, priorLayerErrors[k])) #calc the node's errorSignal
					for h in range(0, inputNN.layers[j].neurons[k].n_inputs):
						deltaWeight(inputNN.layers[j].neurons[k].l_weights[h], learningRate, input[h], priorLayerErrors[k], derivActivation("""unknown inputs  so far"""))
				priorLayerOutput = jLayerOutputK
			priorLayerErrors = jLayerErrors
			counter += 1
		priorLayerErrors = []
		n_iterations += 1
		#calc the error fn for the net?
	return


"""
errorSignal takes ...
returns the error for some given neuron and input
"""
#def errorSignal():
	

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

############################# UPDATE THE FN BELOW AND IMPLIMENT ABOVE...
"""
errorGradientHiddenLayer takes a neuron index for some hidden neuron, n (hiddenN), 
a layer index for this neuron(layerIndex), an error value for the prior layer 
(errorValue), and a neuralNet to which the hiddenN belongs (neuralNet) and returns
the basic error gradient f'n for some hidden neuron.
"""
def errorGradientHiddenLayer(hiddenN, layerIndex, neuralNet, errorValue):
	weights = neuralNet.layers[layerIndex + 1].getWeights()
	sumOut = 0
	for i in range(0, len(weights) + 1):
		for j in range(0, len(weights[i]) + 1):
			sumOut += errorValue * weights[i][j]
	return sumOut

"""
activation takes a neuron (n) and a set of patterns or inputs (p) and returns
the activation value of the neuron on that input pattern.
"""
def activation(p, n):
	activationValue = 0
	for i in range(0, len(p)):
		activationValue += p[i] * n.l_weights[i]
	activationValue += (-1) * l_weights[-1] # threshhold?
	return sigmoid(activationValue)

"""
activation f'ns derivative
"""
#def derivActivation():

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

