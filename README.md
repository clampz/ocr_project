cpat_project
============

this project is for computing practice & theory at the evergreen state college.

this project is in neural networks.

the end goal is to implement optical character recognition.

in order to run, clone the repo and navigate to the clone folder in the command line.

dependancies: python3

there you can change the inputs to the neural network in the params/params.dat subfolder.
then you can run main with 'python main.py'.

components:
============
* main
  * main
  * hasKey
  * todo:
     * need to make prompt and interactivity
* neuralNet
  * neuron
  * neuralNetLayer
  * neuralNet
  * todo:
     * might need some more tools (+ needs real RNG), seems functional otherwise
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
     * need to debug, no learning yet
* fileLib
  * getDataFromFile
  * todo:
     * seems finished

the following sources are the inspiration for the code
i've written and the resources that i've found useful.

Sources:
--------
   - http://www.ibm.com/developerworks/library/l-neural/
   - http://home.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
   - http://www.ai-junkie.com/ann/evolved/nnt1.html
   - http://www.engineering.upm.ro/master-ie/sacpi/mat_did/info068/docum/Neural%20Networks%20for%20Pattern%20Recognition.pdf
   - http://itee.uq.edu.au/~cogs2010/cmc/chapters/BackProp/

