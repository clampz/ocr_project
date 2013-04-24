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

def backProp(max_iterations, error_threshhold):
	n_iterations = 0 #counter for the number of propagation loops
	


def error():



def errorSignal():


def signalError(layer, nodeIndex):





