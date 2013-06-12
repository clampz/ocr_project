import Image
from os import listdir

#imageStorage = []

def displayImage(img):
   x = img.size[0]
   y = img.size[1]
   s = ''
   for i in range(0,y):
      s = s + '\n'
      for j in range(0,x):
         z = img.getpixel((j,i))
         if z > 0:
            s = s + '#'
         else:
            s = s + ' '
   return s

"""
"""
def inverse(lst):
	output = []
	for i in range(0, len(lst)):
		output.append(lst[i] * -1)
	return output

"""
while file is not empty, 
"""
def decomposeParagraph(filename, emptyval = 0):
	while (not isEmptyImage(Image.open(filename), emptyval)):
		cropLargestTopmost(filename, emptyval)
		decomposeLine(filename[0:-4] + 'C.png', emptyval)
		#imageStorage.append(filename[0:-4] + 'C.png')
		filename = filename[0:-4] + 'N.png'

def decomposeLine(filename, emptyval = 0):
	while (not isEmptyImage(Image.open(filename), emptyval)):
		cropLargestLeftMost(filename, emptyval)
		imageStorage.append(filename[0:-4] + 'LN.png')
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
	output.save(filename[0:-4] + 'L.png')
	return output


"""
import Image
from capture import *
from os import listdir
path = '../images/'
image = 'times_new_roman_characters.png'

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

"""

"""
"""
def isEmptyHorizontal(y, img, emptyval = 0):
   for i in range(0, img.size[0]):
      if not isEmptyPixel((i,y), img, emptyval):
        return False
   return True

"""
"""
def isEmptyVertical(x, img, emptyval = 0):
   for i in range(0, img.size[1]):
      if not isEmptyPixel((x,i), img, emptyval):
        return False
   return True

"""
"""
def isEmptyImage(img, emptyval = 0):
	for i in range(0, img.size[1]):
		if not isEmptyHorizontal(i, img, emptyval):
			return False
	return True

def isEmptyPixel((x,y), img, emptyval = 0):
   return img.getpixel((x,y)) == emptyval

def getNeighbors((x,y), cluster, img):
   neighbors = []
   if (x > 0):
      neighbors.append((x-1,y))
   if (x < img.size[0]-1):
      neighbors.append((x+1,y))
   if (y > 0):
      neighbors.append((x,y-1))
   if (y < img.size[1]-1):
      neighbors.append((x,y+1))
   if (x > 0 and y > 0):
      neighbors.append((x-1,y-1))
   if (x > 0 and y < img.size[1]-1):
      neighbors.append((x-1,y+1))
   if (x < img.size[0]-1 and y > 0):
      neighbors.append((x+1,y-1))
   if (x < img.size[0]-1 and y < img.size[1]-1):
      neighbors.append((x+1,y+1))
   neighbors = [item for item in neighbors if item not in cluster]
   return neighbors
      
def getActiveNeighbors(xy, cluster, img):
   return filter(lambda (x,y): not isEmptyPixel((x,y), img), getNeighbors(xy, cluster, img))

def getCluster(xy, img):
   cluster = []
   if (not isEmptyPixel(xy, img)):
      cluster.append(xy)
      cluster += getActiveNeighbors(cluster[0], cluster, img)
      i = 1
      while (i < len(cluster)):
         cluster += getActiveNeighbors(cluster[i], cluster, img)
         i += 1
   return cluster

def firstCluster(img):
   x = img.size[0]
   y = img.size[1]
   myx = 0
   myy = 0
   i = 0
   while (myx != x and myy != y):
      point = (myx, myy)
      cluster = getCluster(point, img)
      if len(cluster) > 0:
         return cluster
      if (myx < x-1):
         i += 1
         myx += 1
      elif (myy < y-1):
         i += 1
         myx = 0
         myy += 1
      else:
         if (myx == x-1 and myy == y-1):
            i += 1
            myx += 1
            myy += 1

def eraseCluster(cluster, img):
   for p in cluster:
      img.putpixel(p, 0)

def maxAndmins(cluster):
   max_x = cluster[0][0]
   min_x = cluster[0][0]
   max_y = cluster[0][1]
   min_y = cluster[0][1]
   for i in range(1,len(cluster)):
      if cluster[i][0] > max_x:
         max_x = cluster[i][0]
      if cluster[i][0] < min_x:
         min_x = cluster[i][0]
      if cluster[i][1] > max_y:
         max_y = cluster[i][1]
      if cluster[i][1] < min_y:
         min_y = cluster[i][1]
   return (min_x, min_y, max_x+1, max_y+1)

def expandPos(x_expand, y_expand, pos):
   posx = pos[0]
   posy = pos[1]
   return (posx + x_expand, posy + y_expand)

def collectCharacters(img):
   x = img.size[0]
   y = img.size[1]
   myx = 0
   myy = 0
   i = 0
   while (myx != x and myy != y):
      point = (myx, myy)
      cluster = getCluster(point, img)
      if len(cluster) > 0:
         print displayImage(im)
         mnm = maxAndmins(cluster)
         print str(mnm)
         newImage = img.crop(mnm)
         print "new size: "+ str(newImage.size[0])
         print "new size2: "+ str(newImage.size[1])
         newImage.load()
         print "Displaying Image"
         print displayImage(newImage)
         print "Name of character:"
         name = raw_input()
         while name == 'grab':
            (t1, t2, t3, t4) = mnm
            print "How far on x-axis from left hand side?"
            dx = input()
            print "How far on y-axis from bottom?"
            dy = input()
            newpoint = expandPos(dx,dy,(t1,t4))
            newCluster = getCluster(newpoint, img)
            print "Cluster length: "+  str(len(newCluster))
            cluster += newCluster
            mnm = maxAndmins(cluster)
            newImage = img.crop(mnm)
            print "new size: "+ str(newImage.size[0])
            print "new size2: "+ str(newImage.size[1])
            newImage.load()
            print "Displaying Image Check"
            print displayImage(newImage)
            print "Name of character:"
            name = raw_input()
         name += '.png'
         newImage.save(name)
         eraseCluster(cluster, img)
      if (myx < x-1):
         i += 1
         myx += 1
      elif (myy < y-1):
         i += 1
         myx = 0
         myy += 1
      else:
         if (myx == x-1 and myy == y-1):
            i += 1
            myx += 1
            myy += 1

def mypaste(fileName, (nx,ny)):
   resize(fileName, (nx,ny))
   img_old = Image.open(fileName)
   cluster = firstCluster(img_old)
   (minx, miny, maxx, maxy) = maxAndmins(cluster) 
   lx = maxx - minx
   ly = maxy - miny
   dx = (nx-lx)/2
   print 'dx: '+str(dx)
   dy = (ny-ly)/2
   print 'dy: '+str(dy)
   cluster = map(lambda (x,y): (x+dx,y+dy), cluster)
   new = Image.new(img_old.mode, (nx,ny), 255)
   for c in cluster:
      new.putpixel(c, 10)
   new.save(fileName)
   

  
def resize(fileName, (nx,ny)):
   img = Image.open(fileName)
   (ix,iy) = img.size
   while (ix*2 <= nx and iy*2 <= ny):
      img = img.resize((ix*2,iy*2), Image.ANTIALIAS)
      #(ix,iy) = img.size
      ix = ix*2
      iy = iy*2
      print str((ix,iy))
   while (ix/2 >= nx and iy/2 >= ny):
      img = img.resize((ix/2,iy/2), Image.ANTIALIAS)
      (ix,iy) = img.size
   img.save(fileName)
   
   #img.thumbnail(newSize, Image.ANTIALIAS)
   #img.save(fileName)


#collectCharacters(im)

#im = Image.open("arial_0.png")
#path = '../images/verdana_characters/'
#files = listdir(path)
#print str(files)
#for i in files:
#   mypaste(path+i, (100,100))
#print 'All done!' 

#= resize('arial_0.png', (100,100))

#collectCharacters(im)

#resize("../images/arial_characters/arial_0.png", (100,100))

#path = '../images/arial_characters/'
#resize(path+'0.png', (100,100))
#img = Image.open('test2.png')
#img = Image.open('test2.png')
#mypaste(img, (100,100))
#print 'done!'
#print str(img.mode)
#a = Image.new(img.mode, (100,100), 255)
#a.save('test3.png')
#a = Image.open('test3.png')
#a.paste(img, (0,0))
#a.save('test3.png')
#a.save('test3.png')
#xs = listdir(path)
#for i in xs:
#   im = Image.open(path+i)
#   print i+': '+str(im.size)
   
