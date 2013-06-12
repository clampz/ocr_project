from random import randrange as rr
import Image
from os import listdir
from re import findall as findall
from math import log as log

class receptor():
	point0 = (0, 0)
	point1 = (0, 0)

"""
a and b are numeric tuples for point0, and point1
"""
	def __init__(self, a, b):
		self.point0 = a
		self.point1 = b

def generate_receptors(img, savefile, x):
   xrs   = []
   yrs   = []
   for i in range(0,x):
      xrs.append(new_x_receptor(img))
      yrs.append(new_y_receptor(img))
   save_receptors(xrs+yrs, savefile)

def tupify(x):
   t = tuple(int(i) for i in findall("[0-9]+", x))
   return (t[0:2],t[2:4])

def save_receptors(receptors, savefile):
   f = open(savefile, 'w')
   s = ""
   for i in receptors:
      s = s +str(i)+"\n"
   f.write(s)
   f.close

def read_receptors(savefile):
   receptors = []
   f = open(savefile, 'r+')
   lines = f.readlines()
   for i in lines:
      receptors.append(tupify(i))
   f.close
   return receptors

def apply_receptors_to_directory(receptor_path, img_dir):
   files = listdir(img_dir)   
   receptors = read_receptors(receptor_path)
   for i in files:
      img = Image.open(img_dir + i)

def new_x_receptor(img):
   (x,y) = img.size
   my_x  = rr(0,x)
   my_y1 = rr(0,y)
   my_y2 = rr(0,y)
   miny  = my_y1
   maxy  = my_y2
   if maxy < miny:
      miny = my_y2
      maxy = my_y1
   start = (my_x,miny)
   end   = (my_x,maxy)
   return (start,end)

def new_y_receptor(img):
   (x,y) = img.size
   my_y  = rr(0,y)
   my_x1 = rr(0,x)
   my_x2 = rr(0,x)
   minx  = my_x1
   maxx  = my_x2
   if maxx < minx:
      minx = my_x2
      maxx = my_x1
   start = (minx,my_y)
   end   = (maxx,my_y)
   return (start,end)

def activate_receptor(img, receptor):
   activated = False
   ((x1,y1),(x2,y2)) = receptor
   if x1 == x2:
      x_rec = True
   else:
      x_rec = False
   current_x = x1
   current_y = y1
   if x_rec:
      for i in range(y1,y2+1):
         if img.getpixel((current_x,i)) == 10:
            return True
   else:
      for i in range(x1,x2+1):
         if img.getpixel((i,current_y)) == 10:
            return True
   return False

def quantify_receptors(receptors, classes):
   courier  = listdir('../images/courier_characters')
   courier.sort()
   times    = listdir('../images/times_new_roman_characters')
   times.sort()
   verdana  = listdir('../images/verdana_characters')
   verdana.sort()
   arial    = listdir('../images/arial_characters')
   arial.sort()
   comic    = listdir('../images/comic_sans_characters')
   comic.sort()

   zlist = zip(courier,times,verdana,arial,comic)

   #Create empty matrix
   matrix = []
   for i in range(0,len(receptors)):
      matrix.append(["R"+str(i)])
      for j in range(0,len(zlist)):
         matrix[i].append([])
   
#   print str(matrix)
   #Fill matrix
   for i in range(0,len(zlist)):
      img = Image.open('../images/courier_characters/'+zlist[i][0])
      for r in range(0,len(receptors)):
         matrix[r][i+1].append(activate_receptor(img, receptors[r]))
      img = Image.open('../images/times_new_roman_characters/'+zlist[i][1])
      for r in range(0,len(receptors)):
         matrix[r][i+1].append(activate_receptor(img, receptors[r]))
      img = Image.open('../images/verdana_characters/'+zlist[i][2])
      for r in range(0,len(receptors)):
         matrix[r][i+1].append(activate_receptor(img, receptors[r]))
      img = Image.open('../images/arial_characters/'+zlist[i][3])
      for r in range(0,len(receptors)):
         matrix[r][i+1].append(activate_receptor(img, receptors[r]))
      img = Image.open('../images/comic_sans_characters/'+zlist[i][4])
      for r in range(0,len(receptors)):
         matrix[r][i+1].append(activate_receptor(img, receptors[r]))
   
   return matrix
   
def inner_entropy(xs):
   ntrue = 0 
   for i in xs:
      if i == True:
         ntrue += 1
   if ntrue == 0 or ntrue == len(xs):
      return 0.0
   else:
      p1 = -(ntrue/(len(xs)*1.0))*log(ntrue/(len(xs)*1.0),2)
      p2 = -((len(xs)-ntrue)/(len(xs)*1.0))*log((len(xs)-ntrue)/(len(xs)*1.0),2)
      return p1+p2

def outer_entropy(col):
   xs = []
   for i in col:
      ntrue = 0
      for j in i:
         if j == True:
            ntrue += 1
      if ntrue >= len(i)/2.0:
         xs.append(True)
      else:
         xs.append(False)
   return inner_entropy(xs)

def average_inner_entropy(col):
   avg = 0
   for i in col:
      avg += inner_entropy(i)
   return avg/len(col)

def calculate_entropy(col):
   return outer_entropy(col) * (1 - average_inner_entropy(col))
   
def matrix_entropy(matrix):
   fitness = []
   for r in matrix:
      fitness.append(calculate_entropy(r[1:len(r)]))
   return fitness
      
#generate 10k receptor dataset
"""   
img = Image.open('arial_a.png')
generate_receptors(img, 'receptors.txt',5000)
print "10k receptors generated"
r = read_receptors('receptors.txt')
classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
m = quantify_receptors(r,classes)
print "10k receptors quantified"
fitness = matrix_entropy(m)
rx = zip(r,fitness)
rx = filter(lambda (x,y): y > 0.8, rx)
rx = map(lambda (x,y): x, rx)
save_receptors(rx, 'iixreceptors.txt')
"""
#generate 100 best receptors
"""
r = read_receptors('iixreceptors.txt')
classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
m = quantify_receptors(r,classes)
fitness = matrix_entropy(m)
rx = zip(r,fitness)
rx.sort(key=lambda tup: tup[1])
rx.reverse()
rx = map(lambda (x,y): x, rx)
best100 = rx[0:100]
save_receptors(best100, 'best100.txt')
"""

