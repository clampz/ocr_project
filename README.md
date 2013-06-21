OCR with Neural Nets
====================

this project is for computing practice & theory at the evergreen state college.

the end goal of this project is to implement optical character recognition for
handwritten characters and to give the unicode equivalents using neural networks.
the current goal of this project is to implement optical character recognition
for computer generated images of text with some fonts.

**dependancies**: python2.7, PIL & pylab. python3 with some small modification

in order to run, download the repo and navigate to the downloaded folder in the command line.

there you can change the inputs to the neural network in the *params* subfolder within the *src* folder. I named
my params file params.dat, so I run my neural net back propagation by typing the following in the command line
```
python main.py -t params.dat
```
The training will save the neural net automatically and it will show up in your params file.

You can run a saved neural net by running a command of the following form. This option will take the most recently written line number for weights data.
```
python main.py -r params.dat neuralNet.dat
```

the majority of the optical character recognition goal is the implementation of
error back propagation training of a neural network. most of that code is in the
propagate module. then there's image preprocessing which mostly happens in the
capture module. the high level image manipulation happens in the main module.

the following sources are the inspiration for the code
i've written and the resources that i have used to understand
the fundamentals of my implementation.

Sources:
--------
   - http://www.codeproject.com/Articles/11285/Neural-Network-OCR
   - http://www.ibm.com/developerworks/library/l-neural/
   - http://home.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
   - http://itee.uq.edu.au/~cogs2010/cmc/chapters/BackProp/

Components:
-----------
* main
  * main
  * runNeuralNet
  * trainNeuralNet
  * imax
  * getClassMatch
  * runNeuralNetImageToText
  * hasKey
  * indent
  * dStruct
* neuralNet
  * neuron
  * neuralNetLayer
  * neuralNet
* propagate
  * backprop
  * sigmoid
  * derivSigmoid
  * errorGradientOutputLayer
  * errorGradientHiddenLayer
  * derivActivation
  * activation
  * y
  * deltaThreshhold
  * deltaWeight
  * sum
  * randLst
* preprocess
  * receptor
* file
  * saveNeuralNet
  * loadNeuralNet
  * saveDataToFile
  * getDataFromFile
  * hasSubString
* capture
  * decomposeParagraph
  * decomposeLine
  * inverse
  * getImageValues
  * cropLargestLeftMost
  * cropLargestTopmost
  * isEmptyHorizontal
  * isEmptyVertical
  * isEmptyImage
  * isEmptyPixel
