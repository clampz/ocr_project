"""

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

def backProp(inputNN, input, max_iterations, error_threshhold):
	n_iterations = 0 # counter for the number of propagation loops
	for i in trainingSet:
		inputNN.update(input)
		for j in range(0, (inputNN.n_hiddenLayers + 2)): # 
			for k in range(0, inputNN.layers[j].n_neurons):
				#calc the weight sum of the inputs to the node
				#calc the activation for the node
		for i in inputNN.layers[-1]:
			#calc the error signal
		for i in range(1, n_hiddenLayers):
			for j in range(0, inputNN.layers[i].n_neurons):
				#calc the node's signal error
				#update each node's weight in the network
		#calc the error fn

def signals(neuron):
	


def error():



def errorSignal(weight):


def signalError(layer, nodeIndex):





