import pygame
import math
from random import randint
import numpy as np

#own imports
from balls import Balls
from pole import Pole
from table import Table

#base class for all scenes
class SceneBase:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.isActive = False

    #functions need to be overwritten
    def start(self):
        print('start needs to be overwritten!')
    def handleEvent(self, events):
        print('handleEvent needs to be overwritten!')
    def update(self):
        print('update needs to be overwritten!')
    def render(self, screen):
        print('render needs to be overwritten!')
    def stop(self):
        print('stop needs to be overwritten!')

#this is the main scene where the game happens
class GameScene(SceneBase):
    def __init__(self, app, width, height):
        SceneBase.__init__(self, app, width, height)

        self.tableWidth = self.width - 100
        self.table = Table(self.tableWidth)
        
        self.aimStart = 0
        self.aimEnd = 0
        self.mousePos = 0

    def start(self):
        self.isActive = True

    def handleEvent(self, events):
        # proceed events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                aimStart = np.array([x, y])
                self.table.pole.aim(aimStart)
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.table.pole.shoot()

            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                mousePos = np.array([x, y])
                self.table.pole.setPos(mousePos)

    def update(self):
        #update all blobs
        self.table.update()

    def render(self, screen):
        screen.fill((255, 255, 255))

        self.table.render(screen, (self.width - self.tableWidth) // 2, 50)

    def stop(self):
        self.isActive = False