import pygame
import numpy as np
import math

class TablePhysics:
    OUTER_WIDTH = 272
    OUTER_HEIGHT = 155
    INNER_WIDTH = 234
    INNER_HEIGHT = 117

    HOLE_WIDTH = 12
    HOLE_HEIGHT = 15


    def __init__(self, width):
        self.width = width
        self.height = (self.width / self.OUTER_WIDTH) * self.OUTER_HEIGHT

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
        self.pointList = self.scalePointList(self.pointList, self.width / self.OUTER_WIDTH)

    def scalePointList(self, pointList, scale):
        newPoints = []
        for point in pointList:
            point = point * scale
            newPoints.append(point)
        return newPoints

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.polygon(screen, (255, 0, 0), self.pointList, 2)