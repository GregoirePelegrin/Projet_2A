import math
import matplotlib.pyplot as plt
import pygame
import time

import Libraries.LibraryGame as lg
import Libraries.LibraryGeneticAlgorithm3 as lga
import Libraries.LibraryNeuralNetwork as lnn

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))

carImg = pygame.image.load("imgs/car.png").convert_alpha()
orientedCarImg = pygame.transform.rotate(carImg, 90)
bg = pygame.image.load("imgs/screen.png").convert()

THRESHOLD = 0.55
NB_CAR = 2
NB_GENERATION = 60
TIME_RACE = 200

DEBUG_MODE = True
PAUSE_MODE = False
VIEW_MODE = True

ga = lga.GeneticAlgorithm(ni=NB_CAR)

cars = []
for i in range(NB_CAR):
    car = lg.Car(i)
    car.orientedCarImg = pygame.transform.rotate(carImg, 90)
    cars.append(car)


pygame.display.set_caption("Racing")
clock = pygame.time.Clock()

gameIsOn = True

x = 350
y = 150
orientation = 90
speed = 0

# CHECKPOINTS
pygame.draw.rect(bg,(0,0,255), (310,130, 20,80))    # center (320,170)
pygame.draw.rect(bg,(0,0,254), (270,430, 20,80))    # center (280,470)
nextCheckpoint = 2
timeRace = time.time()

lastPixel = bg.get_at((int(x),int(y)))

bests, means, nbrIndiv, counters = [], [], [], []

for gen in range(NB_GENERATION):
    timeGen = time.time()
    print("Gen " + str(gen))
    timeCurrent = time.time()

    endGame = 0
    while endGame < TIME_RACE:
        tokenStop = True

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_d :
                    DEBUG_MODE = not DEBUG_MODE
                if event.key == pygame.K_SPACE :
                    PAUSE_MODE = not PAUSE_MODE
                if event.key == pygame.K_v:
                    if VIEW_MODE:
                        for car in cars :
                            car.orientedCarImg = None
                    else :
                        car.orientedCarImg = pygame.transform.rotate(carImg, car.orientation)
                    VIEW_MODE = not VIEW_MODE
        gameDisplay.blit(bg, (0,0))
        for car in cars:
            if(not car.alive):
                continue

            if(car.speed > 0):
                car.speed -= min(0.5, car.speed)
            
            if(car.x >= 0 and car.x < 800 and car.y >= 0 and car.y < 600):
                if(bg.get_at((int(car.x),int(car.y))) == (181, 230, 29, 255)):
                    car.alive = False
                    if(lastPixel != bg.get_at((int(car.x),int(car.y)))):
                        car.speed/=3
                        car.alive = False
                    car.speed -= min(0.45, car.speed)
                if(bg.get_at((int(car.x),int(car.y))) == (0,0,255) and car.nextCheckpoint == 1):
                    print("Finish ! - time = " + str(time.time()-timeRace))
                    car.nextCheckpoint=2
                if(bg.get_at((int(car.x),int(car.y))) == (0,0,254) and car.nextCheckpoint == 2):
                    print("Checkpoint ! - time = " + str(time.time()-timeRace))
                    car.nextCheckpoint=1
                lastPixel = bg.get_at((int(car.x),int(car.y)))
            
            car.orientedCarImg = pygame.transform.rotate(carImg, -car.orientation)
            new_rect = car.orientedCarImg.get_rect(center = (car.x,car.y))

            lineSurface = pygame.Surface((800,600), pygame.SRCALPHA, 32)
            lineSurface = lineSurface.convert_alpha()
            dx = math.cos((car.orientation-90) * math.pi / 180)
            dy = math.sin((car.orientation-90) * math.pi / 180)
            # 2 directions, 45 degrees
            dx2 = math.cos((car.orientation-45) * math.pi / 180)
            dy2 = math.sin((car.orientation-45) * math.pi / 180)
            dx3 = math.cos((car.orientation-135) * math.pi / 180)
            dy3 = math.sin((car.orientation-135) * math.pi / 180)
            dist  = 50
            dist2 = 50
            dist3 = 50
            if(int(car.x+dx*50) >= 0 and int(car.x+dx*50) < 800 and int(car.y+dy*50) >= 0 and int(car.y+dy*50) < 600):
                if(bg.get_at((int(car.x+dx*50),int(car.y+dy*50))) == (181, 230, 29, 255)):
                    while(bg.get_at((int(car.x+dx*dist),int(car.y+dy*dist))) == (181, 230, 29, 255)):
                        dist -= 1
                        if(dist == 0):
                            dist = -1
                            break
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx*50,car.y+dy*50))
                else :
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx*50,car.y+dy*50))
                
            # other directions
            if(int(car.x+dx2*50) >= 0 and int(car.x+dx2*50) < 800 and int(car.y+dy2*50) >= 0 and int(car.y+dy2*50) < 600):
                if(bg.get_at((int(car.x+dx2*50),int(car.y+dy2*50))) == (181, 230, 29, 255)):
                    while(bg.get_at((int(car.x+dx2*dist2),int(car.y+dy2*dist2))) == (181, 230, 29, 255)):
                        dist2 -= 1
                        if(dist2 == 0):
                            dist2 = -1
                            break
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx2*50,car.y+dy2*50))
                else :
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx2*50,car.y+dy2*50))
            
            if(int(car.x+dx3*50) >= 0 and int(car.x+dx3*50) < 800 and int(car.y+dy3*50) >= 0 and int(car.y+dy3*50) < 600):
                if(bg.get_at((int(car.x+dx3*50),int(car.y+dy3*50))) == (181, 230, 29, 255)):
                    while(bg.get_at((int(car.x+dx3*dist3),int(car.y+dy3*dist3))) == (181, 230, 29, 255)):
                        dist3 -= 1
                        if(dist3 == 0):
                            dist3 = -1
                            break
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx3*50,car.y+dy3*50))
                else :
                    VIEW_MODE and DEBUG_MODE and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx3*50,car.y+dy3*50))

            car.totalDistance += car.speed
            if endGame > 30:
                car.lastX = car.x
                car.lastY = car.y
            car.x += dx*car.speed
            car.y += dy*car.speed
            if(car.x < 0 or car.x >= 800 or car.y < 0 or car.y >= 600):
                car.x -= dx*car.speed
                car.y -= dy*car.speed

            VIEW_MODE and gameDisplay.blit(car.orientedCarImg, new_rect.topleft)
            VIEW_MODE and gameDisplay.blit(lineSurface, (0,0))

            listInput = car.nn.evaluate([speed, dist, dist2, dist3])
            if(listInput[0] >= THRESHOLD):
                car.orientation -= 5

            if(listInput[1] >= THRESHOLD):
                car.orientation += 5

            if(listInput[2] >= THRESHOLD):
                car.speed += 1

            if(listInput[3] >= THRESHOLD):
                car.speed -= 0.5

            if car.x != car.lastX or car.y != car.lastY:
                tokenStop = False

        if tokenStop:
            break
        pygame.display.update()
        clock.tick(30)
        endGame += 1
    
    maxDist = 0
    for car in cars :
        maxDist = max(car.totalDistance, maxDist)

    temp_data = ga.evolve(cars)
    bests.append(temp_data[0])
    m = 0
    c = 0
    for fitness in temp_data:
        if fitness == bests[-1]:
            c += 1
        m += fitness
    means.append(m / len(temp_data))
    counters.append(c)
    nbrIndiv.append(len(temp_data))

    print("Best : " + str(round(maxDist, 1)) + ", fps : " +str(round(endGame/(time.time()-timeGen), 1)))

X = [x for x in range(NB_GENERATION)]
ax1 = plt.subplot(211)
ax1.plot(X, bests, label="Bests")
ax1.plot(X, means, label="Means")
ax1.legend()
ax1.grid()
ax1.set_title("Performances")
ax2 = plt.subplot(223)
ax2.plot(X, counters)
ax2.set_title("Nbr of best individuals")
ax2.grid()
ax3 = plt.subplot(224)
ax3.plot(X, nbrIndiv)
ax3.set_title("Nbr of individuals")
plt.show()