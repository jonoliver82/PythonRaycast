import random

class Generator(object):
    """Random Dungeon Generator"""

    FLOOR = '.'
    START = '@'
    DOOR = '+'
    WALL_1 = '9'
    WALL_2 = '3'
    MONSTER = '$'

    START_CHAR_ASCII_A = ord('A') # 65

    def __init__(self):
        self.H = 0
        self.W = 0
        map = [[]]

    def Initialise(self, width, height):
       self.W = width
       self.H = height
       self.map = [['-' for x in range(width)] for y  in range (height)]

    def getWorld(self):
        return self.map
    
    def Run(self):
        self.AddRoom(True)
        for i in range(5000):
            self.AddRoom(False)

    def Draw(self):
        for y in range(self.H):
            for x in range(self.W):
                print(self.map[y][x], end = ' ')

                if x == self.W - 1:
                    print()

    def isWall(value):
        # return str(value).isdigit()
        return value == Generator.WALL_1 or value == Generator.WALL_2

    def isDoor(value):
        return value == Generator.DOOR

    def AddRoom(self, start):
        roomWidth = random.randrange(10) + 5
        roomHeight = random.randrange(6) + 3
        roomX = random.randrange(self.W - roomWidth - 2) + 1
        roomY = random.randrange(self.H - roomHeight - 2) + 1

        # See if its blocked or allowed
        for y in range(roomY - 1, roomY + roomHeight + 2):
            for x in range(roomX - 1, roomX + roomWidth + 2):
                if self.map[y][x] == self.FLOOR:
                    return

        # Add doors
        doorCount = 0
        dx = 0
        dy = 0

        if not start:
            for x in range(roomX, roomX + roomWidth):
                if Generator.isWall(self.map[roomY - 1][x]):
                    doorCount += 1
                    if random.randrange(doorCount) == 0:
                        dx = x
                        dy = roomY  - 1

                if Generator.isWall(self.map[roomY + roomHeight][x]):
                    doorCount += 1
                    if random.randrange(doorCount) == 0:
                        dx = x
                        dy = roomY + roomHeight

            for y in range(roomY, roomY + roomHeight):
                if Generator.isWall(self.map[y][roomX - 1]):
                    doorCount += 1
                    if random.randrange(doorCount) == 0:
                        dx = roomX - 1
                        dy = y
                
                if Generator.isWall(self.map[y][roomX + roomWidth]):
                    doorCount += 1
                    if random.randrange(doorCount) == 0:
                        dx = roomX + roomWidth
                        dy = y

            if doorCount == 0:
                return

        self.AddFloor(roomX, roomWidth, roomY, roomHeight)
        self.AddWalls(roomX, roomWidth, roomY, roomHeight)

        # Draw Door
        if doorCount > 0:
            self.map[dy][dx] = self.DOOR

        # Add start point and things
        for i in range(1 if start else random.randrange(6) + 1):
            if start:
                thing = self.START
            elif random.randrange(4) == 0:
                thing = self.MONSTER
            else:
                thing = random.randrange(10) # chr(self.START_CHAR_ASCII_A + random.randrange(62))
            self.map[random.randrange(roomHeight) + roomY][random.randrange(roomWidth) + roomX] = thing

    def AddFloor(self, roomX, roomWidth, roomY, roomHeight):
        for y in range(roomY, roomY + roomHeight):
            for x in range(roomX, roomX + roomWidth):
                self.map[y][x] = self.FLOOR

    def AddWalls(self, roomX, roomWidth, roomY, roomHeight):
        # origin
        self.map[roomY -1 ][roomX - 1] = self.WALL_1 if roomX + roomY % 2 else self.WALL_2

        # Add Walls X (+1 to include corners)
        for x in range(roomX, roomX + roomWidth + 1):
            self.map[roomY - 1][x] = self.WALL_1 if x % 2 else self.WALL_2
            self.map[roomY + roomHeight][x] = self.WALL_1 if x % 2 else self.WALL_2
        
        # Add Walls Y (+1 to include corners)
        for y in range(roomY, roomY + roomHeight + 1):
            self.map[y][roomX - 1] = self.WALL_1 if y % 2 else self.WALL_2
            self.map[y][roomX + roomWidth] = self.WALL_1 if y % 2 else self.WALL_2