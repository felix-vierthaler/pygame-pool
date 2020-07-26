import pygame
from random import randint, uniform
import math
import cmath
import numpy as np

class Balls:
    RADIUS = 25
    TRIANGLE_SPACING = 5
    

    def __init__(self, width, height):
        self.balls = []
        self.width = width
        self.height = height

    class Ball:
        MASS = 1
        RESISTANCE = 0.0004
        MIN_VEL = 0.1

        def __init__(self, x, y, xV, yV, id, radius):
            self.RADIUS = radius

            self.selected = False

            self.pos = np.array([x, y])
            self.vel = np.array([xV, yV])
            self.id = id

            self.color = (50, 100, 200)
            if id == 0:
                self.color = (245, 245, 245)

            self.font = pygame.font.SysFont("comicsansms", 15)

        def update(self):
            #calculate new velocity with resistance
            velLen = np.linalg.norm(self.vel)

            #simplifyed formula for calculating new velocity with friction
            newVelLen = velLen - math.sqrt(self.RESISTANCE * velLen)

            if newVelLen >= self.MIN_VEL:
                self.vel = (newVelLen / velLen) * self.vel
            else:
                self.vel = np.array([0, 0])

            #update position
            self.pos = self.pos + self.vel

        def render(self, screen):
            #render circle
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.RADIUS)
            if self.selected:
                pygame.draw.circle(screen, (240,250,60), (int(self.pos[0]), int(self.pos[1])), self.RADIUS)

            #render text on ball
            text = self.font.render(str(self.id), True, (0, 0, 0))
            screen.blit(text, (int(self.pos[0]) - text.get_width() / 2, int(self.pos[1]) - text.get_height() / 2))
        
        def collideWith(self, other):
            #information on: https://vobarian.com/collisions/2dcollisions2.pdf

            #find normal vector
            n = other.pos - self.pos
            #calc distance between
            dist = np.linalg.norm(n)

            #if both balls collided
            if dist <= self.RADIUS + other.RADIUS:
                
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
                #move balls apart from each other so they don't collide again
                moveDist = (self.RADIUS + other.RADIUS - dist) / 2
                moveVector = moveDist * un

                self.pos += -moveVector
                other.pos += moveVector
                

    def start(self):
        self.balls.append(self.Ball(600, 600, 0, 0, 0, self.RADIUS))
        self.createTriangle(100,100)
        

    #creates the triangle of balls needed to start a game of 8 ball pool
    def createTriangle(self, xStart, yStart):
        distance = (self.RADIUS * 2) + self.TRIANGLE_SPACING
        height = (distance * 4)
        hDistance = height / 5

        count = 0
        for y in range(5):
            for x in range(y+1):
                count += 1
                
                yPos = yStart + y * hDistance
                xPos = (xStart + x * distance) + ((4 - y) * (distance / 2))

                self.balls.append(self.Ball(xPos, yPos, 0, 0, count, self.RADIUS))


    def mouseDown(self):
        self.balls[0].selected = True

    def mouseUp(self):
        self.balls[0].selected = False

    def getGameBall(self):
        return self.balls[0]

    def shoot(self, aim):
        self.balls[0].vel = aim

    def update(self):
        #check if out of bounds
        for ball in self.balls:
            if ball.pos[0] <= ball.RADIUS:
                ball.vel[0] = ball.vel[0] * -1
                ball.pos[0] = ball.RADIUS
            elif ball.pos[0] > self.width - ball.RADIUS:
                ball.vel[0] = ball.vel[0] * -1
                ball.pos[0] = self.width - ball.RADIUS

            if ball.pos[1] <= ball.RADIUS:
                ball.vel[1] = ball.vel[1] * -1
                ball.pos[1] = ball.RADIUS
            elif ball.pos[1] > self.height - ball.RADIUS:
                ball.vel[1] = ball.vel[1] * -1
                ball.pos[1] = self.height - ball.RADIUS
        
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