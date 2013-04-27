"""
  propagate.py
  by David Weinman
  4/26/13, 9:10p
"""
from neuralNet import *

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
		inputNN.update(input)
		for j in range(0, (inputNN.n_hiddenLayers + 2)): # 
			for k in range(0, inputNN.layers[j].n_neurons):
				#calc the weight sum of the inputs to the node
				#calc the activation for the node
		for j in inputNN.layers[-1]:
			#calc the error signal
		for j in range(1, n_hiddenLayers):# need to find where hidden layers begin in the layers[] array
			for k in range(0, inputNN.layers[j].n_neurons):
				#calc the node's signal error
				#update each node's weight in the network
		#calc the error fn

"""
y takes the same params as target and produces the output for the specified
node in the neural net.
"""
def y(p, n):
	yN = 0 #output value
	if (len(p) != n.n_inputs): # if the node has a different number of inputs than specified in params, throw error.
		raise ValueError('wrong number of inputs: y(p, n) in propagate.')
	for i in range(0, len(p)): # for each input to the node
		yN += p[i] * n.l_weights[i] # sum the value of the input * weight for each input & weight
	return yN




