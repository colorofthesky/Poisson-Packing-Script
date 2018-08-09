###given a closed input curve, spacing, noise, and attractors, output a field of poisson packed points

## imports
import rhinoscriptsyntax as rs
import Rhino as rh
import System.Guid, System.Drawing.Color
import scriptcontext as sc
import time
import math as math
import random as random
from operator import add

# turn off autosave
prevstate = rs.EnableAutosave()
if prevstate == True :
    rs.EnableAutosave(False)

## setup
Width = 300 # width of work area
Height = 300 # height of work area
numberTries = 100 # number of attemps around a point
Radius = 10 # average distance point to point

# set gridCountdownList based on average anaculum radius 

cellSize = Radius * math.sqrt(2)
gridWidth = math.ceil(Width / cellSize)
gridHeight = math.ceil(Height / cellSize)
countDownLength = gridWidth * gridHeight

# pick first point

pointX = random.randrange(0,Width,1)
pointY = random.randrange(0,Height,1)

firstPt = pointX,pointY,0
firstPtGuid = rs.AddPoint(firstPt) #guid of first point

# create ActivePoints list 

activePointList = []
activePointList.append(firstPt) #list of live points
cloudPointList = [] #list of all points including disqualified
cloudPointList.append(firstPt)


 
## Main loop to try for new points

while ( (len(activePointList) >= 1) ):
    
    testPt = activePointList[0]
    del activePointList[0]
    rs.AddPoint(testPt)
    
    
    for testCounter in range(0,numberTries):
        
        # select random vector
        
        vecX = random.random()
        multiX = random.randrange(1,4,1)
        if (multiX > 2):
            multiX = 1
        else:
            multiX = -1
        print "X: " + str(multiX)     
        
        vecY = random.random()
        multiY = random.randrange(1,4,1)
        if (multiY > 2):
            multiY = 1
        else:
            multiY = -1    
        
        vecTest = rs.VectorUnitize( [vecX,vecY,0] )
        vecTest[0] = vecTest[0]*multiX
        vecTest[1] = vecTest[1]*multiY
        vecTest = vecTest * Radius
        
        # transform candidate point
        
        testCoord = [sum(x) for x in zip(testPt,vecTest)]
        testCoord[2] = 0
               #print 'testing the following: ' + str(testCoord)
        
        # test distance to nearest point in pointcloud
        
        
        pointIndex = rs.PointArrayClosestPoint(cloudPointList,testCoord)
        testDistance = rs.Distance(testCoord,cloudPointList[pointIndex])
        #print 'distance equals: ' + str(testDistance)
        
        
        # if point is good add to master and active list
        
        if ((testDistance >= (Radius - 1)) & ( 0 <= testCoord[0] <= Width ) & ( 0 <= testCoord[1] <= Height )) :
            print 'success!'
            rs.AddPoint(testCoord)
            niceCoordTuple = round(testCoord[0],2),round(testCoord[1],2),0
            activePointList.append(niceCoordTuple)
            cloudPointList.append(niceCoordTuple)
            countDownLength -= 1
        
        testCounter += 1
        
        

print cloudPointList
#for cloudPt in cloudPointList:
#    rs.AddPoint(cloudPt)

# Loop to select vector & test for minimum proximity and within boundaries

# If successful, remove 1 from countdown list and add new point to Active Points list

# ElseIf not successful, remove CurrentPoint from ActivePoints list

# when gridCountDownList is 0 end script