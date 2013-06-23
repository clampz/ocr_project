ABSTRACT:
========
* touch on how images with text are broken down in README.md
* refine instructions in README
* refine cl options / interaction & naming, make a man page

Components:
============
* main
  * main
  * trainNeuralNet
  * runNeuralNet
  * imax
  * get_class_match
  * runNeuralNetImageToText
  * hasKey
  * dStruct
  * todo:
     * refine interaction in numeric options, & OCR training
* neuralNet
  * neuron
  * neuralNetLayer
  * neuralNet
  * todo:
     * fix nan in printout
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
  * todo:
     * test hidden layers?
* preprocess
  * receptor
  * todo:
     * finish implementing and start testing, merge with current code
* indenter
  * indenter
  * todo:
     * n/a
* file
  * getDataFromFile
  * saveNeuralNet
  * loadNeuralNet
  * saveDataToFile
  * hasSubString
  * todo:
     * n/a
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
  * todo:
     * n/a


