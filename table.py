import pygame

#own imports
from balls import Balls
from pole import Pole

class Table:
    def __init__(self, width, x, y):
        self.width = width
        self.x = x
        self.y = y

        self.height = int(self.width * 0.5725)  #calc height from width
        self.innerWidth = int(self.width * 0.8550)
        self.spacing = (self.width - self.innerWidth) // 2
        self.innerHeight = self.height - (self.spacing * 2)

        self.surface = 0
        self.preRender()


        self.balls = Balls(self.innerWidth, self.innerHeight)
        self.pole = Pole(self.innerWidth, self.innerHeight, self.balls)

    def update(self):
        self.balls.update()
        self.pole.update()

    def preRender(self):
        self.surface = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.surface, (20, 100, 30), pygame.Rect(0, 0, self.width, self.height))
        pygame.draw.rect(self.surface, (24, 130, 50), pygame.Rect(self.spacing, self.spacing, self.innerWidth, self.innerHeight))

    def render(self, screen):

        ballSurf = pygame.Surface((self.innerWidth, self.innerHeight))
        ballSurf.set_colorkey((0, 0, 0))
        self.balls.render(ballSurf)
        self.pole.render(ballSurf, 0, 0)
        

        screen.blit(self.surface, (self.x, self.y))
        screen.blit(ballSurf, (self.x + self.spacing, self.y + self.spacing))


        


