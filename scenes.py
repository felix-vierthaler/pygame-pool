import pygame
import math
from random import randint
import numpy as np

#own imports
from balls import Balls

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
        
        self.aimStart = 0
        self.aimEnd = 0

    def start(self):
        self.isActive = True

        self.balls.start()

    def handleEvent(self, events):
        # proceed events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.balls.mouseDown()
                x, y = pygame.mouse.get_pos()
                self.aimStart = np.array([x, y])
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.balls.mouseUp()
                x, y = pygame.mouse.get_pos()
                self.aimEnd = np.array([x, y])

                aim = self.aimEnd - self.aimStart
                self.balls.shoot(aim / 30)



    def update(self):
        #update all blobs
        self.balls.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        #pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(100, 100, 300, 300))
        self.balls.render(screen)

    def stop(self):
        self.isActive = False