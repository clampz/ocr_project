"""
  capture.py
  by David Weinman & Jesse Frankley
  6/12/13, 1:37a

---
Contains the functions needed to break
apart an image of computer generated
text and yield images of the characters
in the given image (namely, decomposeParagraph),
and the function needed to get an array of
inputs to a neural net from an image of a
character (getImageValues).
"""

"""
This file is licensed under the MIT License, see LICENSE for details.
"""

import Image
import os

"""
takes a list of numbers and returns the same list with each value
multiplied by -1
"""
def inverse(lst):
	output = []
	for i in range(0, len(lst)):
		output.append(lst[i] * -1)
	return output

"""
takes an image file name (filename) and returns the numerical
value of each pixel in an array
"""
def getImageValues(filename):
	im = Image.open(filename)
# got IOError once IOError("cannot identify image file") when images got overwritten?
	output = []
	for i in range(0, im.size[1]):
		for j in range(0, im.size[0]):
			try:
				output.append(im.getpixel((i, j)))
			except IndexError:
				pass
	return output

"""
takes an image file name (filename), a tuple indicating the size of images
of characters to end up as ((sizex, sizey)), an image storage array
(imageStorage), and a background RGB value emptyval which defaults to 0 if
not specified. the function breaks up the line(s) of characters in the image
into images of characters.
"""
def decomposeParagraph(filename, (sizex, sizey), imageStorage, emptyval = 0):
	while (not isEmptyImage(Image.open(filename), emptyval)):
		cropLargestToMost(filename, emptyval)
		decomposeLine(filename[0:-4] + 'C.png', imageStorage, emptyval)
		filename = filename[0:-4] + 'N.png'
#		cleanupList.append(filename[0:-4] + 'N.png')
#		cleanupList.append(filename[0:-4] + 'C.png')
	ls = os.listdir(os.getcwd())
	for i in ls:
		if ((filename[0:-4] + 'C' in i) or (filename[0:-4] + 'N' in i)) and ('.png' in i) and (not 'L.png' in i):
			os.remove(i)
#	print('\n' + str(cleanupList) + '\n')
#	for i in cleanupList:
#		try:
#			remove(i)
#		except OSError:
#			print("capture -> decomposeLine -> warning: no such file: %s" % i)
	for i in imageStorage:
		im = Image.open(i)
		newImage = im.resize((sizex, sizey))
		newImage.save(i)

"""
does the same as the function above except it breaks up lines, and it doesn't resize images.
"""
def decomposeLine(filename, imageStorage, emptyval = 0):
	while (not isEmptyImage(Image.open(filename), emptyval)):
		cropLargestLeftMost(filename, emptyval)
		imageStorage.append(filename[0:-4] + 'L.png')
		filename = filename[0:-4] + 'LN.png'

"""
takes the name of a .png file (filename) and a
background color (emptyval), saves a new image
of the leftmost character of the given file
in a new file and returns the image object saved.
"""
def cropLargestLeftMost(filename, emptyval = 0):
	im = Image.open(filename)
	left = top = right = counter = 0
	lower = im.size[1]
	for i in range(0, im.size[0] - 1):
		if i != 0 and ((not isEmptyVertical(i, im, emptyval)) != (not isEmptyVertical(i - 1, im, emptyval))):
			if counter > 0:
				right = i + 1
				break
			counter += 1
	for i in range(0, im.size[0] - 1):
		if i != 0 and ((not isEmptyVertical(i, im, emptyval)) != (not isEmptyVertical(i - 1, im, emptyval))):
			left = i - 1
			break
	output = im.crop((left, top, right, lower))
	nextImage = im.crop((right, 0, im.size[0], im.size[1]))
	nextImage.save(filename[0:-4] + 'LN.png')
	right = output.size[0]
	left = 0
	counter = 0
	for i in inverse(range(-(output.size[1] - 2), 0)):
		if i != 0 and ((not isEmptyHorizontal(i, output, emptyval)) != (not isEmptyHorizontal(i + 1, output, emptyval))):
			lower = i + 2
			break
	for i in range(0, output.size[1]):
		if i != 0 and ((not isEmptyHorizontal(i, output, emptyval)) != (not isEmptyHorizontal(i - 1, output, emptyval))):
			top = i - 1
			break
	output = output.crop((left, top, right, lower))
	try:
		output.save(filename[0:-4] + 'L.png')
	except SystemError:
		print('capture -> cropLargestLeftMost; warning: couldn\'t save ' + filename[0:-4] + 'L.png')
	return output
"""
cropLargestLeftMost
"""

"""
cropLargestTopmost takes an image filename and a background value (emptyval)
and saves a new file with the topmost line of text cropped out
"""
def cropLargestTopmost(filename, emptyval = 0):
# open the image and make some default values in case the algorithm can't seperate anything from the edges of the image
	im = Image.open(filename)
	left = upper = counter = 0
	right = im.size[0] - 1
	lower = im.size[1] - 1
# iterate from the top edge and count spaces in order to make a bottom to crop
	for i in range(0, (im.size[1] - 1)):
# compare Emptiness as it goes along
		if i != 0 and ((not isEmptyHorizontal(i, im, emptyval)) != (not isEmptyHorizontal(i + 1, im, emptyval))):
			if counter > 0:
				lower = i + 2
				break
			counter += 1
# iterate from the top
	for i in range(0, im.size[1]):
		if i != 0 and ((not isEmptyHorizontal(i, im, emptyval)) != (not isEmptyHorizontal(i - 1, im, emptyval))):
			upper = i - 1
			break
	#print('output = im.crop((%d le, %d u, %d r, %d lo))' % (left, upper, right, lower))
	output = im.crop((left, upper, right, lower))
	output.save(filename[0:-4] + 'C.png')
	nextCrop = im.crop((0, lower - 1, im.size[0], im.size[1]))
	nextCrop.save(filename[0:-4] + 'N.png')
"""
cropLargestTopMost
"""

"""
takes an int y index (y) where y is an index in im.size[1],
an image object (img), and a background value (emptyval) which
defaults to 0 and returns a boolean representation of whether
or not the horizontal is all background values.
"""
def isEmptyHorizontal(y, img, emptyval = 0):
   for i in range(0, img.size[0]):
      if not isEmptyPixel((i,y), img, emptyval):
        return False
   return True

"""
isEmptyVertical takes an int x index (x) where x is an index in
im.size[0], an image object (img), and a background value (emptyval)
which defaults to 0 and returns a boolean representation of whether
or not the vertical is all background values.
"""
def isEmptyVertical(x, img, emptyval = 0):
   for i in range(0, img.size[1]):
      if not isEmptyPixel((x,i), img, emptyval):
        return False
   return True

"""
isEmptyImage takes an image object (img), and a background value
(emptyval) which defaults to 0 and returns a boolean representation
of whether or not the image object is empty.
"""
def isEmptyImage(img, emptyval = 0):
	for i in range(0, img.size[1]):
		if not isEmptyHorizontal(i, img, emptyval):
			return False
	return True

"""
isEmptyPixel takes a pair of ints representing the pixels location
((x,y)), an image object img, and a background value (emptyval) which
defaults to 0 and returns True if it's the emptyval and false if not.
"""
def isEmptyPixel((x,y), img, emptyval = 0):
   return img.getpixel((x,y)) == emptyval

