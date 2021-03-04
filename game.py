import pygame
import math
import time

import LibraryNeuralNetwork as lnn

THRESHOLD = 0.6
nn = lnn.NeuralNetwork(size=[2, 5, 5, 4])

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("Racing")
clock = pygame.time.Clock()

gameIsOn = True

carImg = pygame.image.load("imgs/car.png")
orientedCarImg = pygame.transform.rotate(carImg, 90)
bg = pygame.image.load("imgs/screen.png")


x = 350
y = 150
accelerationH = 0
accelerationV = 0
currentV = 0
currentH = 0
orientation = 90
acceleration = 0


# CHECKPOINTS
pygame.draw.rect(bg,(0,0,255), (310,130, 20,80))    # center (320,170)
pygame.draw.rect(bg,(0,0,254), (270,430, 20,80))    # center (280,470)
nextCheckpoint = 2
timeRace = time.time()

possibleActions = ["UP", "DOWN", "RIGHT", "LEFT"]
environnement = [-1]
actions = []

lastPixel = bg.get_at((int(x),int(y)))

while(gameIsOn):

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            gameIsOn = False
            print("Game is off")
        
    keys = pygame.key.get_pressed()

    new_rect = orientedCarImg.get_rect(center = (x,y))
    if(keys[pygame.K_LEFT]):
        #carImg = pygame.transform.rotate(carImg, -10)
        orientation -= 5
        actions.append("LEFT")

    if(keys[pygame.K_RIGHT]):
        #carImg = pygame.transform.rotate(carImg, 10)
        orientation += 5
        actions.append("RIGHT")

    if(keys[pygame.K_UP]):
        acceleration += 1
        actions.append("UP")

    if(keys[pygame.K_DOWN]):
        acceleration -= 0.5
        actions.append("DOWN")
    
    if(acceleration > 0):
        acceleration -= min(0.5, acceleration)
    
    if(x >= 0 and x < 800 and y >= 0 and y < 600):
        if(bg.get_at((int(x),int(y))) == (181, 230, 29, 255)):
            if(lastPixel != bg.get_at((int(x),int(y)))):
                acceleration/=3
            acceleration -= min(0.45, acceleration)
        if(bg.get_at((int(x),int(y))) == (0,0,255) and nextCheckpoint == 1):
            print("Finish ! - time = " + str(time.time()-timeRace))
            nextCheckpoint=2
            print(actions)
            actions = []
        if(bg.get_at((int(x),int(y))) == (0,0,254) and nextCheckpoint == 2):
            print("Checkpoint ! - time = " + str(time.time()-timeRace))
            nextCheckpoint=1
        lastPixel = bg.get_at((int(x),int(y)))
    
    orientedCarImg = pygame.transform.rotate(carImg, -orientation)
    new_rect = orientedCarImg.get_rect(center = (x,y))

    lineSurface = pygame.Surface((800,600), pygame.SRCALPHA, 32)
    lineSurface = lineSurface.convert_alpha()
    dx = math.cos((orientation-90) * math.pi / 180)
    dy = math.sin((orientation-90) * math.pi / 180)
    dist = 50
    if(int(x+dx*50) >= 0 and int(x+dx*50) < 800 and int(y+dy*50) >= 0 and int(y+dy*50) < 600):
        if(bg.get_at((int(x+dx*50),int(y+dy*50))) == (181, 230, 29, 255)):
            while(bg.get_at((int(x+dx*dist),int(y+dy*dist))) == (181, 230, 29, 255)):
                dist-=1
                if(dist==0):
                    break
            pygame.draw.line(lineSurface, (255,0,0),(x,y),(x+dx*50,y+dy*50))
            environnement[0] = dist
        else : 
            pygame.draw.line(lineSurface, (0,255,0),(x,y),(x+dx*50,y+dy*50))
            environnement[0] = -1

    x += dx*acceleration
    y += dy*acceleration
    if(x < 0 or x >= 800 or y < 0 or y >= 600):
        x -= dx*acceleration
        y -= dy*acceleration

    gameDisplay.blit(bg, (0,0))
    gameDisplay.blit(orientedCarImg, new_rect.topleft)
    gameDisplay.blit(lineSurface, (0,0))
    pygame.display.update()
    #pygame.display.flip()
    listInput = nn.evaluate([acceleration, dist])

    if(listInput[0] >= THRESHOLD):
        #carImg = pygame.transform.rotate(carImg, -10)
        orientation -= 5
        actions.append("LEFT")

    if(listInput[1] >= THRESHOLD):
        #carImg = pygame.transform.rotate(carImg, 10)
        orientation += 5
        actions.append("RIGHT")

    if(listInput[2] >= THRESHOLD):
        acceleration += 1
        actions.append("UP")

    if(listInput[3] >= THRESHOLD):
        acceleration -= 0.5
        actions.append("DOWN")

    clock.tick(30)

    