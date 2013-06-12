#A simple script meant to demonstrate the results of a 625_39 backpropagation trained neuralnetwork for OCR.

import NN2
import Image
import os
import numpy as np
from capture import *

imageStorage = []

def imax(xs):
   m = max(xs)
   return [i for i, j in enumerate(xs) if j == m]

def get_class_match(xs):
   classes     = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
   return classes[imax(xs)[0]]

theta = np.array(NN2.load_theta('625_39_ocr_theta.txt'))


#img = Image.open('images/arial_characters/arial_v.png')

#original_input = Image.open('images/' + sys.argv[1])

decomposeParagraph('images/' + sys.argv[1])

for i in imageStorage:
	img = Image.open('images/' + i)
	X = np.array(list(img.getdata()))
	print get_class_match(NN2.runNet(theta,[625,39],X)[0])

