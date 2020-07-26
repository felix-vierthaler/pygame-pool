#this is a representation of all the states a ball can be
class BallStatus:
    black = 1
    white = 2
    stripe = 3
    solid = 4

#stores all the different colors, numbers and statuses of the balls.
class BallDesign:
    YELLOW = (255, 255, 4)
    BLUE = (0, 0, 250)
    RED = (250, 0, 0)
    PURPLE = (155, 4, 255)
    ORANGE = (255, 139, 4)
    GREEN = (3, 152, 22)
    BURGUNDY = (154, 2, 17)
    BLACK = (5, 5, 5)
    WHITE = (253, 253, 253)

    def __init__(self):
        self.designs = []
        self.generateDesigns()

    def generateDesigns(self):
        self.designs.append(self.Design("", self.WHITE, BallStatus.white))  #white ball id=0

        self.designs.append(self.Design("1", self.YELLOW, BallStatus.solid))
        self.designs.append(self.Design("9", self.YELLOW, BallStatus.stripe))

        self.designs.append(self.Design("2", self.BLUE, BallStatus.solid))
        self.designs.append(self.Design("10", self.BLUE, BallStatus.stripe))


        self.designs.append(self.Design("", self.BLACK, BallStatus.black))  #black ball id=8


        self.designs.append(self.Design("3", self.RED, BallStatus.solid))
        self.designs.append(self.Design("11", self.RED, BallStatus.stripe))

        self.designs.append(self.Design("4", self.PURPLE, BallStatus.solid))
        self.designs.append(self.Design("12", self.PURPLE, BallStatus.stripe))

        self.designs.append(self.Design("5", self.ORANGE, BallStatus.solid))
        self.designs.append(self.Design("13", self.ORANGE, BallStatus.stripe))

        self.designs.append(self.Design("6", self.GREEN, BallStatus.solid))
        self.designs.append(self.Design("14", self.GREEN, BallStatus.stripe))

        self.designs.append(self.Design("7", self.BURGUNDY, BallStatus.solid))
        self.designs.append(self.Design("15", self.BURGUNDY, BallStatus.stripe))


    def getDesign(self, id):
        return self.designs[id]

    class Design:
        def __init__(self, name, color, status):
            self.name = name
            self.color = color
            self.status = status
