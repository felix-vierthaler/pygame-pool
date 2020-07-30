import pygame
from random import randint, uniform
import math
import cmath
import numpy as np

from ballDesign import BallDesign, BallStatus

class Balls:
    RADIUS = 25
    TRIANGLE_SPACING = 0
    
    def __init__(self, width, height):
        self.balls = []
        self.width = width
        self.height = height

        self.start()

    class Ball:
        MASS = 1
        RESISTANCE = 0.0002
        BORDER_RESISTANCE = 0.3
        MIN_VEL = 0.1

        
        TEXT_MARGIN = 6
        STRIPE_MARGIN = 6

        FONT_COLOR = (1, 1, 1)

        def __init__(self, x, y, xV, yV, id, radius):

            self.design = BallDesign().getDesign(id)

            self.RADIUS = radius
            self.TEXT_SIZE = int(self.RADIUS / 2.5)

            self.pos = np.array([x, y])
            self.vel = np.array([xV, yV])
            self.id = id

            self.font = pygame.font.SysFont("comicsansms", self.TEXT_SIZE)
            self.surface = 0
            self.createSurface()

        #creates the surface of the ball before game starts. doesnt have to rerender on every frame
        def createSurface(self):
            #create new survace
            self.surface = pygame.Surface((self.RADIUS*2, self.RADIUS*2))
            self.surface.set_colorkey((0,0,0))  #dont blit black pixels
            #render circle
            pygame.draw.circle(self.surface, self.design.color, (self.RADIUS, self.RADIUS), self.RADIUS)

            #if theres more to do than just the colors
            if self.design.status == BallStatus.stripe or self.design.status == BallStatus.solid:
                if self.design.status == BallStatus.stripe:
                    #create new surface to construct striped ball because it is made up of weird shapes
                    whiteSurface = pygame.Surface((self.RADIUS*2, self.RADIUS*2))
                    whiteSurface.set_colorkey((0,0,0))  #dont blit black pixels
                    pygame.draw.circle(whiteSurface, (255, 255, 255), (self.RADIUS, self.RADIUS), self.RADIUS)
                    #calculate width of stripe on ball
                    stripeWidth = self.TEXT_SIZE + (self.TEXT_MARGIN * 2) + (self.STRIPE_MARGIN * 2)
                    pygame.draw.rect(whiteSurface, (0, 0, 0), pygame.Rect(0, self.RADIUS - stripeWidth // 2, self.RADIUS * 2, stripeWidth))
                    self.surface.blit(whiteSurface, (0, 0))

                #render white circle on ball
                pygame.draw.circle(self.surface, (255, 255, 255), (self.RADIUS, self.RADIUS), int(self.TEXT_SIZE/2 + self.TEXT_MARGIN))

                #render text on ball
                text = self.font.render(self.design.name, True, self.FONT_COLOR)
                self.surface.blit(text, (int(self.RADIUS - (text.get_width() / 2)), int(self.RADIUS - (text.get_height() / 2))))

        def update(self):
            #calculate new velocity with resistance
            velLen = np.linalg.norm(self.vel)

            #simplifyed formula for calculating new velocity with friction
            newVelLen = velLen - math.sqrt(self.RESISTANCE * velLen)

            #if new velocity greater than min velocity, calc new velocity vector
            if newVelLen >= self.MIN_VEL:
                self.vel = (newVelLen / velLen) * self.vel
            else:
                self.vel = np.array([0, 0])

            #update position
            self.pos = self.pos + self.vel

        def render(self, screen):
            screen.blit(self.surface, (int(self.pos[0] - self.RADIUS), int(self.pos[1] - self.RADIUS)))
        
        #calculates physics of two colliding balls
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

        def mirror(self, mirrorVector, moveBy):  


            un = mirrorVector / np.linalg.norm(mirrorVector)
            ut = np.array([-un[1], un[0]])

            unProj = np.dot(un, self.vel)
            utProj = np.dot(ut, self.vel)

            utProj = utProj * -1
            utProj = utProj * ut
            utProj = utProj - (utProj * self.BORDER_RESISTANCE)
            unProj = unProj * un


            self.vel = utProj + unProj
            self.pos += ut * moveBy
                
    def start(self):
        self.balls.append(self.Ball(600, 500, 0, 0, 0, self.RADIUS))
        self.createTriangle(600, 232)
        
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

    #returns the game Ball
    def getGameBall(self):
        return self.balls[0]

    #sets new velocity of the game ball
    def shoot(self, aim):
        self.balls[0].vel = aim

    def getMaybeIntersectingBalls(self, verSpacing, horSpacing):
        #check if ball is out of bounds
        intersectingBalls = []
        for ball in self.balls:
            if np.linalg.norm(ball.vel) > 0:
                intersecting = False
                if ball.pos[0] <= ball.RADIUS + horSpacing:
                    intersecting = True
                elif ball.pos[0] > self.width - ball.RADIUS - horSpacing:
                    intersecting = True
                if ball.pos[1] <= ball.RADIUS + verSpacing:
                    intersecting = True
                elif ball.pos[1] > self.height - ball.RADIUS - verSpacing:
                    intersecting = True

                if intersecting:
                    intersectingBalls.append(ball)

        return intersectingBalls

    #updates all balls in the array accordingly
    def update(self):
        #update every ball
        for ball in self.balls:
            ball.update()
        
        #check for collisions between balls and handle inside Ball class
        for x in range(0, len(self.balls) - 1):
            for y in range(x + 1, len(self.balls)):
                ball1 = self.balls[x]
                ball2 = self.balls[y]
                ball1.collideWith(ball2)

    #renders all balls on screen
    def render(self, screen):
        for ball in self.balls:
            ball.render(screen)