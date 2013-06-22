README.md
* touch on how images with text are broken down

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
     * want to make visualization (ui ?), need to refine cl options
* neuralNet
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
  * randLst
  * todo:
     * test neural nets with hidden layers
* preprocess
  * receptor
  * todo:
     * finish implementing and start testing, merge with current code
* indenter
  * indenter
* file
  * getDataFromFile
  * saveNeuralNet
  * loadNeuralNet
  * saveDataToFile
  * hasSubString
  * todo:
     * looks done for now
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
     * need to merge code into a cl option


