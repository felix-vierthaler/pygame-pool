import pygame
import math
from random import randint
import numpy as np

#own imports
from balls import Balls
from pole import Pole

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


class GameScene(SceneBase):
    def __init__(self, app, width, height):
        SceneBase.__init__(self, app, width, height)

        self.balls = Balls(self.width, self.height)
        self.pole = Pole(self.width, self.height, self.balls)
        
        self.aimStart = 0
        self.aimEnd = 0
        self.mousePos = 0

    def start(self):
        self.isActive = True

        self.balls.start()

    def handleEvent(self, events):
        # proceed events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                aimStart = np.array([x, y])
                self.pole.aim(aimStart)
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.pole.shoot()

            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                mousePos = np.array([x, y])
                self.pole.setPos(mousePos)



    def update(self):
        #update all blobs
        self.balls.update()
        self.pole.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        #pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(100, 100, 300, 300))
        self.balls.render(screen)
        self.pole.render(screen)

    def stop(self):
        self.isActive = False