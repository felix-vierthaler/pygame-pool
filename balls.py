import pygame
from random import randint, uniform
import math
import cmath
import numpy as np

class Balls:
    def __init__(self, width, height):
        self.balls = []
        self.width = width
        self.height = height

    class Ball:
        RADIUS = 25
        MASS = 1

        def __init__(self, x, y, xV, yV, name):
            self.pos = np.array([x, y])
            self.vel = np.array([xV, yV])
            self.name = name

            self.font = pygame.font.SysFont("comicsansms", 15)

            self.collided = False

        def update(self):
            #update position
            self.pos = self.pos + self.vel

        def render(self, screen):
            pygame.draw.circle(screen, (255, 155, 11), (int(self.pos[0]), int(self.pos[1])), self.RADIUS)
            #render text on ball
            text = self.font.render(str(self.name), True, (0, 128, 0))
            screen.blit(text, (self.pos[0] - text.get_width() / 2, self.pos[1] - text.get_height() / 2))
            



        #https://vobarian.com/collisions/2dcollisions2.pdf

        def collideWith(self, other):
            #find normal vector
            n = other.pos - self.pos
            #calc distance between
            dist = np.linalg.norm(n)

            #if both balls collided
            if dist <= self.RADIUS + other.RADIUS:
                self.collided = True
                
                #find unit normal vector
                un = n * (1 / dist)

                #find unit tangent vector
                ut = np.array([- un[1], un[0]])
                
                #vel 1 normal and tangient vector
                v1n = np.dot(self.vel, un)
                v1t = np.dot(self.vel, ut)

                #vel 2 normal and tangient vector
                v2n = np.dot(other.vel, un)
                v2t = np.dot(other.vel, ut)

                """
                print('--elastic collision debugging--')
                print('normal vector: ', n)
                print('distance: ', dist)
                print('unit normal vector: ', un)
                print('unit tangient vector: ', ut)
                print('v1n: ', v1n)
                print('v1t: ', v1t)
                print('v2n: ', v2n)
                print('v2t: ', v2t)
                """

                #calc normal vector, assuming that both masses are the same --> just switch both
                tmp = v1n
                v1n = v2n
                v2n = tmp

                #make vectors from the scalars again
                v1n = v1n * un
                v1t = v1t * ut

                v2n = v2n * un
                v2t = v2t * ut

                #add tangential and normal vector to calc final velocity
                v1 = v1n + v1t
                v2 = v2n + v2t

                self.vel = v1
                other.vel = v2

                """
                print('switch v1n and v2n')
                print('v1n: ', v1n)
                print('v1t: ', v1t)
                print('v2n: ', v2n)
                print('v2t: ', v2t)
                print('calc velocities')
                print('v1: ', v1)
                print('v2: ', v2)
                """

    def start(self):

        for i in range(20):
            self.balls.append(self.Ball(randint(0, self.width), randint(0, self.height), uniform(0, 3), uniform(0, 3), i))


    def update(self):
        
        #check if out of bounds
        for ball in self.balls:
            if ball.pos[0] <= 0 + ball.RADIUS or ball.pos[0] > self.width - ball.RADIUS:
                ball.vel[0] = ball.vel[0] * -1

            if ball.pos[1] <= 0 + ball.RADIUS or ball.pos[1] > self.height - ball.RADIUS:
                ball.vel[1] = ball.vel[1] * -1
        
        #check for collisions
        for x in range(0, len(self.balls) - 1):
            for y in range(x + 1, len(self.balls)):
                ball1 = self.balls[x]
                ball2 = self.balls[y]
                ball1.collideWith(ball2)

        for ball in self.balls:
            ball.update()

    def render(self, screen):
        for ball in self.balls:
            ball.render(screen)