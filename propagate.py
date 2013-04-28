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
def backProp(inputNN, input, max_iterations, error_threshhold):
	n_iterations = 0 # counter for the number of propagation loops
	for i in trainingSet:
		y = inputNN.update(input) # present the pattern to the network
		for j in range(0, (inputNN.n_hiddenLayers + 2)):
			for k in range(0, inputNN.layers[j].n_neurons):
				weightSumK = sum(inputNN.layers[j].neurons[k].l_weights) #calc the weight sum of the inputs to the node
				activationK = activation(inputToNeuron, inputNN.layers[j].neurons[k]) #calc the activation for the node
		for j in inputNN.layers[-1]:
			#calc the error signal
		for j in range(1, n_hiddenLayers):# need to find where hidden layers begin in the layers[] array
			for k in range(0, inputNN.layers[j].n_neurons):
				#calc the node's signal error
				#update each node's weight in the network
		#calc the error fn

"""
errorSignal takes ...
returns the error for some given neuron and input
"""
#def errorSignal():
	

"""
y takes a set of patterns or inputs (p), and a neuron (n) and returns the 
output for the specified node in the neural net. [keep in mind that the output
of some neuron is dependent upon which layer it is in.]
"""
def y(p, n):
	if (len(p) != n.n_inputs): # if the node has a different number of inputs than specified in params, throw error.
		raise ValueError('wrong number of inputs: y(p, n) in propagate.')
	return sigmoid(activation(p, n))

"""
sigmoid takes an activation value (activation) and calculates the sigmoid 
function on the activation value
"""
def sigmoid(activation):
        return 1/float(1 + (math.e**((-activation) / 1.0))) # where curve shape or 'p' is set to 1.0

"""
sigmoid f'ns derivative.
"""
def derivSigmoid(activation):
	return sigmoid(activation) * (1 - sigmoid(activation))

"""
errorGradient takes an output of some neuron, n (outputN) and a target
value for the same neuron, n (targetN) and produces the basic error gradient
f'n for some output neuron. [this f'n is specific to the output layer of neurons]
"""
def errorGradientOutputLayer(outputN, targetN):
	return outputN * (1 - outputN) * (targetN - outputN)

"""
errorGradientHiddenLayer takes an output of some neuron, n (outputN) and a
target value for the same neuron, n (targetN) and a 
"""

"""
activation takes a neuron (n) and a set of patterns or inputs (p) and returns
the activation value of the neuron on that input pattern.
"""
def activation(p, n)
	activationValue = 0
	for i in range(0, len(p)):
		activationValue += p[i] * n.l_weights[i]
	activationValue += (-1) * l_weights[-1] # threshhold?
	return activationValue

"""
deltaThreshhold takes a target value for some pattern (targetP), an output value 
for some pattern; for some node (outputP) and returns the change in threshhold value
for that input on that node.
"""
def deltaThreshhold(targetP, outputP):
	return (-1) * (targetP - outputP)

"""
deltaWeight takes a target value for some pattern (targetP), an output value 
for some pattern; for some node (outputP), an input value for some pattern
for the same node and returns the change in weight for that input on that node.
"""
def deltaWeight(targetP, outputP, inputPI):
	return (targetP - outputP) * inputPI

"""
sum takes a list of numbers and returns the sum of a list of numbers.
"""
def sum(lst):
	if (len(lst) == 1):
		return lst[0]
	else:
		return lst[0] + sum(lst[1:])


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

