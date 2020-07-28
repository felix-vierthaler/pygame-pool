import pygame

#own imports
from balls import Balls
from pole import Pole
from tablePhysics import TablePhysics

class Table:

    def __init__(self, width):
        self.width = width
        
        self.tablePhysics = TablePhysics(self.width)
        self.height = self.tablePhysics.height
        self.balls = Balls(self.width, self.height)

        self.pole = Pole(self.balls)

        self.preRender()

    def update(self):
        self.balls.update()
        self.pole.update()

        self.tablePhysics.intersectingLines = []
        for ball in self.balls.getMaybeIntersectingBalls(self.tablePhysics.horSpacing, self.tablePhysics.verSpacing):
            
            mirrorVectors = self.tablePhysics.getMirrorVektor(ball.pos, ball.RADIUS)
            for mirrorVector in mirrorVectors:
                ball.mirror(mirrorVector[0], mirrorVector[1])

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


        


