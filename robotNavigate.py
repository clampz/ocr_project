"""
GOAL: make a scribbler navigate a maze
ALGORITHM: Behavior Based Control
8/2/12
written by david weinman & tylerwhite
ver2.0
"""

"""
ALGORITHM NOTES:

----
algorithm for making the 4 points around an obstacle:

when the wall on any side of an object is past, record the location as true in the map.

----
algorithm for stopping at the start point of an obstacle:

record the location when the robot finds an object. the robot should plan a trajectory 
back to this point either when it has finished mapping the object or given up on mapping it.
"""

"""
PARAMETERS:
	End goal (ordered pair of coordinates)
	Turn calibration
	Distance calibration
"""

"""
BEHAVIORS:

	Update the map <- done
	Build a trajectory <- done
	Homing <- not done
	See and measure objects to build them in the map <- not done
	Motor and distance calibration <- done
	Chooses optimal paths <- not done

"""

import sys#sys module provides os f'ns
import math#math module provides math f'ns like cosine and float to keep precision
from myro import *#myro module provides f'ns to operate the robot and collect sensor data
from time import *#time module provides f'ns to to keep track of time and stopwatch functionality

#this class keeps track of the robots position, orientation, and end goal.
class roboPos():
	xPos = 0
	yPos = 0
	orientation = 0
	map = {}
	endGoal = []
	breadcrumbs = []
	turnCalibration = []# [leftMotor, rightMotor]
	distanceCalibration = []# [leftMotor, rightMotor]

	def __init__ (self):
		self.orientation = 90
		self.xPos = 0
		self.yPos = 0
		self.endGoal = [0,25]
		self.breadcrumbs = [[0,0]]
		# the robot starts at the origin by default, so its set to false here
		self.map['[0,0]'] = False
		self.turnCalibration = [0,0]
		self.distanceCalibration = [0,0]
		return

	def getOrient(self):# returns the robots orientation in degrees.
		return self.orientation

	def getPos(self):# returns a list containing the robots position in the form [x,y].
		return [float(self.xPos), float(self.yPos)]

	def rightTurn(self, angle):# keeps track of the robots orientation involved in a right turn.
		self.orientation -= angle
		print 'I turned, my new orientation is: %d' % self.orientation
		return

	def leftTurn(self, angle):# keeps track of the robots orientation involved in a left turn.
		self.orientation += angle
       		print 'I turned, my new orientation is: %d' % self.orientation
    		return

    	def setTurnCalibration(self,leftTurn, rightTurn):
		self.turnCalibration = [leftTurn, rightTurn]
		return

	def setDistanceCalibration(self, leftMotor, rightMotor):
		self.distanceCalibration = [leftMotor, rightMotor]
		return

	def setMap(self, pairString, value):#setMap takes a string containing a list of two values
		self.map[pairString] = value#in the form [x,y] and puts a value, True or False in it.
		return
	
	def getMap():
		return map
	
	def getCoord(pairString):
		return map[pairString]

	def setPos(self, x, y):# used to set the new position of the robot. setPos(xCoord,yCoord)
		self.xPos = float(x)
		self.yPos = float(y)
		self.breadcrumbs.append([float(x), float(y)])
		return [float(x),float(y)]



"""
########################################################################################
#------------------------------------------------ MAP OPERATION FUNCTIONS
########################################################################################
"""

"""
buildTrajectory takes a list of two numbers representing the end point and returns a 
list containing an angle that the robot needs to turn to and the difference in the
robots current angle plus the needed angle for the heading
"""
def buildTrajectory(endPosition):
	adjacent = endPosition[0] - robot.getPos()[0]# do these two lines need float()?
	opposite = endPosition[1] - robot.getPos()[1]
	theta = math.degrees(math.atan(opposite/float(adjacent))) * -1
	return [theta, (robot.getOrient() - theta)]

"""
this f'n keeps track of the location of the robot, Boolean tells whether the
robot is going forward, True -> Forward, False -> Backwards. roboDocumentOrientation
returns the position in the form of a list with two elements.
"""
def roboDocumentOrientation(directionBoolean, objectBoolean):
        angle = robot.getOrient()
        position = robot.getPos()
        if directionBoolean == False:#if boolean is false, triangle math needs to do a 180.
                angle += 180
#do triangle math. update the robot object's position and the map.
        robot.setMap(str(robot.setPos((position[0] + math.cos(math.radians(angle))),(position[1] + math.sin(math.radians(angle))))), objectBoolean)
        print 'documenting... old: %s, new: %s' % (position, robot.getPos())
        return robot.getPos()



"""
########################################################################################
#------------------------------------------------ MOVEMENT FUNCTIONS
########################################################################################
"""

"""
calibrated motor turn values
8 /23 / 12 : motors value for a 1 degree turn is .585
8 /29 / 12 : .68
TODAY: .59
"""
#makes the robot go right 1 degree and updates its position.
def roboTurnRight(angle):
	robot.rightTurn(angle)
	for i in range(angle):
		motors(float(robot.turnCalibration[0]),0)
		sleep(.001)
		stop()
	return

"""
calibrated motor turn values
8 /23 / 12 : motors value for a 1 degree turn is .499
8 /29 / 12 : .589
TODAY: .568
"""
#makes the robot turn left and updates its position.
def roboTurnLeft(angle):
	robot.leftTurn(angle)
	for i in range(angle):
		motors(0,float(robot.turnCalibration[1]))
		sleep(.001)
		stop()
	return

"""
calibrated motor distance values
TODAY: R: .95 L: 1
"""
#this function makes the robot move forward one inch
def goFoward(objectBoolean):
	motors(robot.distanceCalibration[0],robot.distanceCalibration[1])
	sleep(.01)
	stop()
	roboDocumentOrientation(True, objectBoolean)
	return

#makes the robot back up one inch and updates its position.
def roboBackUp(objectBoolean):
	roboDocumentOrientation(False, objectBoolean)
	backward(1,.68)
	stop()
	return

#goMeasured() tells the robot to go forward by 'inches' distance.
def goMeasured(inches):
	for i in range(inches):
		goFoward(False)
	return

#function will take a variable angle and reposition robot to the given angle
def roboAcidBurn(angie):
	brad = angie - robot.getOrient()
	if brad < 0:
		roboTurnRight(abs(brad))
	if brad > 0:
		roboTurnLeft(brad)
	return

"""
########################################################################################
#------------------------------------------------ MOTOR AND DISTANCE CALIBRATION
########################################################################################
"""

#asks the user if the robot had the desired effect. stringInput is the raw_input() param.
def askUser(stringInput):
	try:
		output =  eval(raw_input(stringInput))
	except NameError:
		pass
	try:	
		if output == True:
			return False
	except UnboundLocalError:
		pass
	return True

#------------------------------------------------ LINEAR CALIBRATION
# ask the user for the calibrated distance values.
def calibrateDistance(): 
	print '\nLet\'s calibrate the forward movement. This is intended to move the robot forward one inch.\n'
	while askUser('\ndid the robot move forward one inch? (respond with either True or False): '):
		right = eval(raw_input('pick the right motor\'s speed: '))
		left = eval(raw_input('pick the left motor\'s speed: '))
		for i in range(4):
			forwardCalibration(left,right)
	robot.setDistanceCalibration(left, right)
	return

"""
incrementForward is intended to calibrate the and trajectory of a forward movement
l is the left motors speed and likewise r -> right motor speed
"""
def forwardCalibration(l,r):
	motors(float(l),float(r))
	sleep(.01)
	stop()
	return


#------------------------------------------------ TURN CALIBRATION
"""
this function asks the user for a motor value, executes the loop f'n
keeps asking the
user for motor values until the user responds that 
the robot executed a 90 degree turn
"""
def calibrateMotors():
	print '\nLet\'s calibrate the right motor. This will execute 90 degree left turns.\n'
	while askUser('\ndid the robot execute a 90 degree turn? (respond with either True or False): ') :
		inputNumberRight = eval(raw_input('Pick a motor input: '))
		loop(inputNumberRight, True)
	print '\nLet\'s calibrate the left motor. This will execute 90 degree right turns.\n'
	while askUser('\ndid the robot execute a 90 degree turn? (respond with either True or False): ') :
		inputNumberLeft = eval(raw_input('Pick a motor input: '))
		loop(inputNumberLeft, False)
	robot.setTurnCalibration(inputNumberLeft,inputNumberRight)
	return
		


#run increment 90 times to execute a 90 degree turn T -> left turns F -> right turns
def loop(x, rightOrLeftTurn):
	for i in range(90):
		if rightOrLeftTurn:
			incrementLeftTurn(x)
		else:
			incrementRightTurn(x)
	return

"""
these functions (incrementLeftTurn & incrementRightTurn) are intended to 
calibrate the motor speed (x) needed for a one degree turn in .001 of a second
"""

def incrementRightTurn(x):
		motors(float(x),0)
		sleep(.001)
		stop()
		return

def incrementLeftTurn(x):
		motors(0,float(x))
		sleep(.001)
		stop()
		return

"""
########################################################################################
#------------------------------------------------ OBSTACLE BUILDING FOR MAPS
########################################################################################
"""

#makes robot turn away from object depending on what side of wall it is on
def tooCloseWallFollowing(TLDR):
	if TLDR:
		roboTurnRight(3)	
	else:
		roboTurnLeft(3)
	return

#makes robot turn toward object depending on what side of wall it is on
def getCloserWallFollowing(LtR):
	if LtR :
		roboTurnLeft(3)
	else:
		roboTurnRight(3)
	return	

"""
 followWall() makes the robot follow a wall until it can't find the given wall any longer.
 then it documents the corner in the maps
 leftOrRight = T->R , F->L
"""
def followWall(leftOrRight):	
	sensorIndex = 0
	if leftOrRight :#the wall is to the right of the robot if this evaluates true
		sensorIndex = 2
	sum = getAllSensorAvg()[sensorIndex]
	while sum > 0 :# this condition seems like it needs some changing.
		sum = getAllSensorAvg()[sensorIndex]# get some sensor readings
		if (99 < sum) and (sum < 1000):#just at the right distance
			goMeasured(1)
			print 'Im moving forward'
		elif (sum < 101) and (sum > 20):
			getCloserWallFollowing(leftOrRight)#too far away from wall
			sum = getAllSensorAvg()[sensorIndex]
			print 'Im turning toward the object'
		elif sum > 1000:
			tooCloseWallFollowing(leftOrRight)#too close to wall
			sum = getAllSensorAvg()[sensorIndex]
			print 'Im turning away from the object'
		else:#passed wall.
			print 'I\'m done with this wall. movin\' on'
			goMeasured(5)
			if leftOrRight:
				roboTurnRight(90)
			else:
				roboTurnLeft(90)
			robot.setMap(str(robot.breadcrumbs[-3]), True)
			break
	return

"""
########################################################################################
#------------------------------------------------ OBSTACLE SENSOR DATA FUNCTIONS
########################################################################################
"""

#get the average of all 3 sensors. returns a list of the form [leftSensor,centerSensor,rightSensor]
def getAllSensorAvg():
	return [getSensorAvg(0),getSensorAvg(1),getSensorAvg(2)]

"""
getSensorAvg gets the average value of some given sensor. returns the average value for 
five readings of the given sensor.
"""
def getSensorAvg(sensorIndex):
#obstacleList is given the sensor data in the form [leftSensor,centerSensor,rightSensor]
	obstacleList = getObstacle()
	sensorList = [0,0,0,0,0]
	sum = 0
	for i in range(5):
		obstacleList = getObstacle()
		sensorList[i] = obstacleList[sensorIndex]
		sum += sensorList[i]
	return (sum / 5)

"""
########################################################################################
#------------------------------------------------ MISCELLANEOUS FUNCTIONS
########################################################################################
"""

#this f'n returns true while the goal has not been reached, and false when the goal is reached.
def roboGoal():
	if robot.getPos() != robot.endGoal:
		return True
	return False

#this is the condition function used to decide when to move based on sensor data
def conditionSensors(sensorAvg):
	if ((sensorAvg[0] > 500) or (sensorAvg[1] > 500) or (sensorAvg[2] > 500)):
		return True
	return False

#initializes the robo.
def bootUpOrShutUp():
	init()
	print 'ReneRobo: boot up or shut up.'
	return

#main function is choosing what the robot will do for the demo.
def main():
	bootUpOrShutUp()
	calibrateDistance()
	calibrateMotors()
	raw_input('\npress any key when you\'re ready to follow walls.: ')
	rOrL = eval(raw_input('1 for wall on right of robot, 2 for left: '))
	followWall(rOrL)
	strInput = 'follow another wall? 1: y 2: n: '
	if (eval(raw_input(strInput))):#2nd time?
		followWall(rOrL)
		if (eval(raw_input(strInput))):#3rd time?
			followWall(rOrL)
			if (eval(raw_input(strInput))):#4th time?
				followWall(rOrL)
	return

robot = roboPos()
main()

"""
########################################################################################
#----------------------------------------------------------COPYPASTA
########################################################################################

#makes the robot go straight and updates its position.
def roboGoStraight():
	roboDocumentOrientation(True)
	motors(.8,.8)
	sleep(.25)
	stop()
	return

"""
