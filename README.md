OCR with Neural Nets
====================

this project is for computing practice & theory at the evergreen state college.

the end goal of this project is to implement optical character recognition for
handwritten characters and to give the unicode equivalents using neural networks.
the current goal of this project is to implement optical character recognition
for computer generated images of text with some fonts.

**dependancies**: python2.7 or python3 with some small modification

in order to run, download the repo and navigate to the downloaded folder in the command line.

there you can change the inputs to the neural network in the *params* subfolder. I named
my params file params.dat, so I run my neural net back propagation by typing the following in the command line
```
python main.py -t params.dat
```
In the training prompt you have the option to save your weights. The line number at which the weights were saved will be written in the params file with the time and date when you saved the weights.

You can run a saved neural net by running a command of the following form. This option will take the most recently written line number for weights data.
```
python main.py -r params.dat neuralNet.dat
```

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
