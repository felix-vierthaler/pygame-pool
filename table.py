import pygame

#own imports
from balls import Balls
from pole import Pole
from tablePhysics import TablePhysics

class Table:

    def __init__(self, width):
        self.width = width

        self.createTable()
        
        

        self.tablePhysics = TablePhysics(self.width)
        self.height = self.tablePhysics.height
        self.balls = Balls(self.width, self.height)

        self.pole = Pole(self.balls)

        self.preRender()

    def createTable(self):
        pass

    def update(self):
        self.balls.update()
        self.pole.update()

    def preRender(self):
        self.surface = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.surface, (55, 236, 85), pygame.Rect(0, 0, self.width, self.height))

    def render(self, screen, x, y):

        tableSurf = pygame.Surface((self.width, self.height))
        tableSurf.blit(self.surface, (0, 0))

        self.balls.render(tableSurf)

        self.tablePhysics.render(tableSurf)

        screen.blit(tableSurf, (x, y))

        self.pole.render(screen, x, y)


        


