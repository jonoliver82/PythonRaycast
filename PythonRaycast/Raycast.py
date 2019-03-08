import random
import math
from utilities import *
from time import *
from Generator import Generator

class Raycast(object):
    """Simple Raycaster"""
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 200

    DOOR_COLOR = 'dark gray'

    WORLD_BLOCK_SIZE = 10
    PLAYER_START_ANGLE_DEGREES = 90
    PLAYER_ROTATE_DEGREES_AMOUNT = 5
    PLAYER_STEP_AMOUNT = 2.0
    RADIANS_CONVERSION_FACTOR = math.pi / 180    
    SCREEN_CENTER_Y = SCREEN_HEIGHT / 2
    DRAW_LINE_WIDTH = 5
    FIELD_OF_VIEW_DEGREES = 60
    HALF_FIELD_OF_VIEW_DEGREES = FIELD_OF_VIEW_DEGREES / 2
    ANGLE_INCREMENT_DEGREES = (FIELD_OF_VIEW_DEGREES / SCREEN_WIDTH) * DRAW_LINE_WIDTH

    cosTable = [None] * 360;
    sinTable = [None] * 360;

    def __init__(self, world, canvas):
        self.world = world
        self.canvas = canvas

        # locate start character        
        y,x = index2d(self.world, Generator.START)
        self.playerX = (x + 0.5) * Raycast.WORLD_BLOCK_SIZE
        self.playerY = (y + 0.5) * Raycast.WORLD_BLOCK_SIZE
        
        self.playerFacingDegrees = Raycast.PLAYER_START_ANGLE_DEGREES

        for i in range(0, 360):
            self.cosTable[i] = math.cos(i * Raycast.RADIANS_CONVERSION_FACTOR)
            self.sinTable[i] = math.sin(i * Raycast.RADIANS_CONVERSION_FACTOR)

    def keypress(self, key):
        if key.keysym == 'd' or key.keysym == 'Right':
            self.playerFacingDegrees = (self.playerFacingDegrees + Raycast.PLAYER_ROTATE_DEGREES_AMOUNT) % 360

        if key.keysym == 'a' or key.keysym == 'Left':
            self.playerFacingDegrees = (self.playerFacingDegrees + (360 - Raycast.PLAYER_ROTATE_DEGREES_AMOUNT)) % 360

        if key.keysym == 'w' or key.keysym == 'Up':
            newPlayerX = self.playerX + (self.cosTable[self.playerFacingDegrees] * Raycast.PLAYER_STEP_AMOUNT)
            newPlayerY = self.playerY + (self.sinTable[self.playerFacingDegrees] * Raycast.PLAYER_STEP_AMOUNT)
            self.tryUpdatePlayerPosition(newPlayerX, newPlayerY)

        if key.keysym == 's' or key.keysym == 'Down':
            newPlayerX = self.playerX - (self.cosTable[self.playerFacingDegrees] * Raycast.PLAYER_STEP_AMOUNT)
            newPlayerY = self.playerY - (self.sinTable[self.playerFacingDegrees] * Raycast.PLAYER_STEP_AMOUNT)
            self.tryUpdatePlayerPosition(newPlayerX, newPlayerY)

    def tryUpdatePlayerPosition(self, x,y):
        if Generator.isWall(self.world[int((y / Raycast.WORLD_BLOCK_SIZE))][int((x / Raycast.WORLD_BLOCK_SIZE))]) == False:
            self.playerX = x
            self.playerY = y

    def drawWall(self, x, halfWallHeight, itemColor):
        # x1,y1,x2,y2
        fillColor = self.DOOR_COLOR if Generator.isDoor(itemColor) else COLORS[int(itemColor)]
        self.canvas.create_rectangle(x, Raycast.SCREEN_CENTER_Y - halfWallHeight, x + Raycast.DRAW_LINE_WIDTH,  Raycast.SCREEN_CENTER_Y + halfWallHeight, width=0, fill=fillColor) 

    def drawFloor(self, x, halfWallHeight):
        # x1,y1,x2,y2
        self.canvas.create_rectangle(x, Raycast.SCREEN_CENTER_Y + halfWallHeight, x + Raycast.DRAW_LINE_WIDTH,  Raycast.SCREEN_HEIGHT, width=0, fill='gray')  

    def drawCeiling(self, x, halfWallHeight):
        # x1,y1,x2,y2
        self.canvas.create_rectangle(x, 0, x + Raycast.DRAW_LINE_WIDTH,  Raycast.SCREEN_CENTER_Y - halfWallHeight, width=0, fill='black')  

    def raycast(self):
        # looking right
        for rayAngleDegrees in frange(self.playerFacingDegrees, self.playerFacingDegrees + Raycast.FIELD_OF_VIEW_DEGREES, Raycast.ANGLE_INCREMENT_DEGREES):
            xIncrement = self.cosTable[int(rayAngleDegrees % 360)]
            yIncrement = self.sinTable[int(rayAngleDegrees % 360)]

            testX = self.playerX;
            testY = self.playerY;
            rayLength = 1
            blockColor = 0

            try:
                while Generator.isWall(blockColor) == False and Generator.isDoor(blockColor) == False:
                    testX += xIncrement
                    testY += yIncrement
                    rayLength += 1
                    worldX = int((testX / Raycast.WORLD_BLOCK_SIZE))
                    worldY = int((testY / Raycast.WORLD_BLOCK_SIZE))
                    blockColor = self.world[worldY][worldX]
            except IndexError as msg:
                print(msg)

            # remove door when near
            if Generator.isDoor(blockColor) and rayLength < Raycast.WORLD_BLOCK_SIZE:
                self.world[worldY][worldX] = Generator.FLOOR

            # set start x for rectangles
            x = ((rayAngleDegrees - self.playerFacingDegrees) * Raycast.DRAW_LINE_WIDTH) / Raycast.ANGLE_INCREMENT_DEGREES

            # compensate for fisheye view as ray is cast from center
            beta = rayAngleDegrees - self.playerFacingDegrees - Raycast.HALF_FIELD_OF_VIEW_DEGREES
            rayLength = rayLength * math.cos(beta * Raycast.RADIANS_CONVERSION_FACTOR)

            # scale the wall according to distance, if the rayLength is shorter then the wall must be drawn bigger
            wallHeight = (1000 / rayLength) * 2
            if wallHeight > Raycast.SCREEN_HEIGHT:
                wallHeight  = Raycast.SCREEN_HEIGHT

            halfWallHeight = wallHeight / 2

            self.drawCeiling(x, halfWallHeight)
            self.drawWall(x, halfWallHeight, blockColor)
            self.drawFloor(x, halfWallHeight)

    def render(self):
        start_time = int(round(time() * 1000))
        self.raycast()
        end_time = int(round(time() * 1000))
        render_time = round(end_time - start_time)
        # print('Render Time:', render_time)
        self.canvas.after(render_time, self.render)