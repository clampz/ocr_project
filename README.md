OCR with Neural Nets
====================

this project is for computing practice & theory at the evergreen state college.

the end goal of this project is to implement optical character recognition for
handwritten characters and to give the unicode equivalents using neural networks.

**dependancies**: python3, or python2.7

in order to run, download the repo and navigate to the downloaded folder in the command line.

there you can change the inputs to the neural network in the *params* subfolder. I named
my params file params.dat, so I run my neural net by typing the following in the command line

```
python main.py params.dat
```

Components:
============
* main
  * main
  * hasKey
  * indent
  * todo:
     * need to make prompt and interactivity + visualization (ui ?)
* neuralNet
  * receptor
  * neuron
  * neuralNetLayer
  * neuralNet
  * todo:
     * might need some more tools, implement receptors
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
  * todo:
     * test neural nets with hidden layers
* fileLib
  * getDataFromFile
  * todo:
     * nothing
* imagePreProcessing
  * PIL
  * todo:
     * need to implement

the following sources are the inspiration for the code
i've written and the resources that i've found useful.

Sources:
--------
   - http://www.ibm.com/developerworks/library/l-neural/
   - http://home.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
   - http://www.ai-junkie.com/ann/evolved/nnt1.html
   - http://www.engineering.upm.ro/master-ie/sacpi/mat_did/info068/docum/Neural%20Networks%20for%20Pattern%20Recognition.pdf
   - http://itee.uq.edu.au/~cogs2010/cmc/chapters/BackProp/

