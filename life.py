#!/usr/bin/python
import sys, random, copy
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from guerillaDisplay import *
import logging
import RPi.GPIO as GPIO
import os

# AnextY live cell with fewer than two live neighbors dies, as if by underpopulation.
# AnextY live cell with two or three live neighbors lives on to the next generation.
# AnextY live cell with more than three live neighbors dies, as if by overpopulation.
# AnextY dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

#LBO shutdown PIN
PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('--%(levelname)s--%(message)s')
#file handler
fileHandler = logging.FileHandler('guerillaLife.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
#Disable requests logging unless 'warning'
logging.getLogger("urllib3").setLevel(logging.WARNING)

def getNeighbors(generation, x, y):
    upperX = len(generation[0])-1
    upperY = len(generation)-1
    neighborCount = 0
    nextX = 0
    nextY = 0
    #n1 = x-1;y-1
    if x == 0:
        #!n1
        pass
    else:
        nextX = x - 1
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n1

    #n2 = x;y-1
    if x == 0:
        #!n2
        pass
    else:
        nextX = x
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n2

    #n3 = x+1;y-1
    if x == upperX or y == 0:
        #!n3
        pass
    elif y == upperY:
        #!n3
        pass
    else:
        nextX = x + 1
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n3

    #n4 = x+1;y
    if y == upperY or x == upperX:
        #!n4
        pass
    else:
        nextX = x + 1
        nextY = y
        neighborCount += generation[nextY][nextX] #n4

    #n5 = x+1;y+1
    if y == upperY or x == upperX:
        #!n5
        pass
    else:
        nextX = x + 1
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n5

    #n6 = x;y+1
    if x == upperX or y == upperY:
        #!n6
        pass
    else:
        nextX = x
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n6

    #n7 = x-1;y+1
    if x == 0 or y == upperY:
        #!n7
        pass
    else:
        nextX = x - 1
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n7

    #n8 = x-1;y
    if x == 0:
        #!n8
        pass
    else:
        nextX = x - 1
        nextY = y
        neighborCount += generation[nextY][nextX] #n8

    return neighborCount

def runLife(xsize, ysize, sprinkle, seed = None):
    #randomize Color
    cellR = random.randint(128,255)
    cellG = random.randint(128,255)
    cellB = random.randint(128,255)
    logger.info(" colors: %s, %s, %s",cellR,cellG,cellB)
    #build grid
    gridRow, trackPulsar, trackBlinker, generationX, generationY, theseed = ([] for i in range(6))
    for x in range(0,xsize):
        gridRow.append(0)
    for y in range(0,ysize):
        theseed.append(copy.deepcopy(gridRow))

    trackPulsar = copy.deepcopy(theseed)
    trackBlinker = copy.deepcopy(theseed)
    generationX = copy.deepcopy(theseed)
    generationY = copy.deepcopy(theseed)

    #seed the grid
    if seed:
        #we got a seed here!
        pass
    else:
        #randomly seed
        for y in range(0,ysize):
            for x in range(0,sprinkle):
                ranCell = random.randint(0,xsize-1)
                generationX[y][ranCell] = theseed[y][ranCell] = 1

        #record the seed
        logger.info(" --------- THE SEED ---------")
        for r in generationX:
            row = ""
            for c in r:
                if c == 0:
                    row = row + " "
                if c == 1:
                    row = row + "*"
            logger.info(row)

        tick = 1
        dead = 0
        while not dead:
            imalive = 0
            frozen = 1
            blinking = 1
            pulsar = 1
            for x in range(0,xsize):
                for y in range(0,ysize):
                    if generationX[y][x] == 1:
                        imalive = 1
                    neighbors = getNeighbors(generationX,x,y)
                    #die
                    if generationX[y][x] == 1 and neighbors < 2:
                        generationY[y][x] = 0
                        gd.cellOff(x,y)
                    if generationX[y][x] == 1 and neighbors > 3:
                        generationY[y][x] = 0
                        gd.cellOff(x,y)
                    #live
                    if generationX[y][x] == 1 and (neighbors == 2 or neighbors == 3):
                        generationY[y][x] = 1
                        gd.cellOn(x,y,cellR,cellG,cellB)
                    #birth
                    if generationX[y][x] == 0:
                        if neighbors == 3:
                            generationY[y][x] = 1
                            gd.cellOn(x,y,cellR,cellG,cellB)

            #clear screen
            #gd.clear()

            #show current tick
            logger.info(" --------- Tick: %s ---------", tick)
            for r in generationX:
                row = ""
                for c in r:
                    if c == 0:
                        row = row + " "
                    if c == 1:
                        row = row + "*"
                logger.info(row)
            #computer next tick
            tick += 1
            for x in range (0,xsize):
                for y in range(0,ysize):
                    if trackPulsar[y][x] != generationY[y][x]:
                        pulsar = 0
                    if trackBlinker[y][x] != generationY[y][x]:
                        blinking = 0
                    if generationX[y][x] != generationY[y][x]:
                        frozen = 0
            #watch for blinkers/pulsars
            if(not tick % 7):
                trackPulsar = copy.deepcopy(generationX)
            if(not tick % 3):
                trackBlinker = copy.deepcopy(generationX)
            generationX = copy.deepcopy(generationY)

            if not imalive or frozen or blinking or pulsar:
                dead = 1
                if not imalive:
                    cause = "Death"
                elif frozen:
                    cause = "Frozen"
                elif blinking:
                    cause = "Blinking"
                elif pulsar:
                    cause = "Pulsar"
                logger.info(" -----")
                logger.info(" Total Generations: %s || Termination Cause: %s", tick, cause)
                logger.info(" -----")
                gd.clear()


gd = guerillaDisplay()
gd.initiate()

while True:
    runLife(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    time.sleep(0.5)

    #Check for low power
    logger.info('LBO Status: %s',GPIO.input(PIN))
    if not GPIO.input(PIN):
      logger.warning("Low Battery Power Detected.  Shutting down...")
      GCD.off()
      os.system("sudo shutdown --poweroff")
