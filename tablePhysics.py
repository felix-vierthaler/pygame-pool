import pygame
import numpy as np
from numpy.linalg import norm 
import math
import sys

class TablePhysics:
    OUTER_WIDTH = 272
    OUTER_HEIGHT = 155
    INNER_WIDTH = 234
    INNER_HEIGHT = 117

    HOLE_WIDTH = 18  #12
    HOLE_HEIGHT = 18  #15

    def __init__(self, width):
        self.width = width

        scaleFactor = self.width / self.OUTER_WIDTH
        self.height = scaleFactor * self.OUTER_HEIGHT
        self.horSpacing = (self.OUTER_WIDTH - self.INNER_WIDTH) / 2 * scaleFactor
        self.verSpacing = (self.OUTER_HEIGHT - self.INNER_HEIGHT) / 2 * scaleFactor

        #calculate dynamic dimensions from static dimensions
        self.HOR_SPACING = (self.OUTER_WIDTH - self.INNER_WIDTH) // 2
        self.VER_SPACING = (self.OUTER_HEIGHT - self.INNER_HEIGHT) // 2

        self.HOLE_WIDTH_T = math.sqrt(1/2) * self.HOLE_WIDTH
        self.HOLE_HEIGHT_T = math.sqrt(1/2) * self.HOLE_HEIGHT
        
        #point on upper left inner edge to start calculations from
        startPoint = np.array([self.HOR_SPACING, self.VER_SPACING])
        
        #create list of points for physical calculation
        self.pointList = []

        #calculate upper left part of table
        p1 = np.array([startPoint[0], startPoint[1] + self.HOLE_WIDTH_T])  #P1
        p2 = np.array([p1[0] - self.HOLE_HEIGHT_T, p1[1] - self.HOLE_HEIGHT_T])  #P2
        p3 = np.array([p2[0] + self.HOLE_WIDTH_T, p2[1] - self.HOLE_WIDTH_T])  #P3
        p4 = np.array([startPoint[0] + self.HOLE_WIDTH_T, startPoint[1]])  #P4
        p5 = np.array([startPoint[0] + self.INNER_WIDTH / 2 - self.HOLE_WIDTH / 2, startPoint[1]])  #P5
        p6 = np.array([p5[0], p5[1] - self.HOLE_HEIGHT])  #P5

        self.pointList.append(p1)
        self.pointList.append(p2)
        self.pointList.append(p3)
        self.pointList.append(p4)
        self.pointList.append(p5)
        self.pointList.append(p6)

        #mirror existing points on y axis and add to array in reverse order
        for point in reversed(self.pointList):
            newPoint = np.array([self.OUTER_WIDTH - point[0], point[1]])
            self.pointList.append(newPoint)
        #mirror existing points on x axis and add to array in reverse order
        for point in reversed(self.pointList):
            newPoint = np.array([point[0], self.OUTER_HEIGHT - point[1]])
            self.pointList.append(newPoint)

        #scale all the points to fit the given width
        self.pointList = self.scalePointList(self.pointList, scaleFactor)


        self.intersectingLines = []

    def scalePointList(self, pointList, scale):
        newPoints = []
        for point in pointList:
            point = point * scale
            newPoints.append(point)
        return newPoints

    def calcDistPointToLine(self, p1, p2, p3):
        return abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))


    def isCircleInLine(self, p1, p2, p3, radius):
        intersecting = False

        intersectionLength = self.calcDistPointToLine(p1, p2, p3) - radius
        

        if intersectionLength <= 0:
            
            lineDir = p1-p2

            #calculate vector diagonal to the line
            diagonalVec = np.array([-lineDir[1], lineDir[0]])
            
            #create points diagonal to line from line points
            dp1 = p1 + diagonalVec
            dp2 = p2 + diagonalVec
            #calc parallel distances from input point to new lines
            dLineDist1 = self.calcDistPointToLine(p1, dp1, p3)
            dLineDist2 = self.calcDistPointToLine(p2, dp2, p3)
            #calc distances from input point to line points
            lineDist1 = np.linalg.norm(p1 - p3)
            lineDist2 = np.linalg.norm(p2 - p3)

            #check if ball is on line
            if dLineDist1 + dLineDist2 <= np.linalg.norm(p2-p1) + 1:
                intersecting = True
            

            elif lineDist1 <= radius or lineDist2 <= radius:
                intersecting = True

        return intersecting, intersectionLength * -1

    def getMirrorVektor(self, point, radius):
        mirrorVektors = []
        for i in range(0, len(self.pointList)):

            #get both points of the line
            p1 = self.pointList[i]
            p2Index = i + 1
            if p2Index >= len(self.pointList):
                p2Index = 0
            p2 = self.pointList[p2Index]

            intersecting, howMuch = self.isCircleInLine(p1, p2, point, radius)
            
            if intersecting:
                #print("line: ", i, " dist: ", dist, " p1: ", p1, " p2: ", p2, " point: ", point, " cross: ", cross)

                #collision occured
                connVector = p2 - p1
                mirrorVektors.append((connVector, howMuch))
                self.intersectingLines.append((p1, p2))
                break

        return mirrorVektors

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.pointList, 2)

        for line in self.intersectingLines:
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 2)




#only if this file is executed as main
if __name__ == "__main__":
    tablePhysics = TablePhysics(1000)
    
    