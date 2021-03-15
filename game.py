import math
import matplotlib.pyplot as plt
import pygame
import time

import Libraries.LibraryGame as lg
import Libraries.LibraryGeneticAlgorithm2 as lga
import Libraries.LibraryNeuralNetwork as lnn


carImg = pygame.image.load("imgs/car.png")
orientedCarImg = pygame.transform.rotate(carImg, 90)
bg = pygame.image.load("imgs/screen.png")

THRESHOLD = 0.55
NB_CAR = 10
NB_GENERATION = 30
TIME_RACE = 1

ga = lga.GeneticAlgorithm(ni=NB_CAR)

cars = []
for i in range(NB_CAR):
    car = lg.Car(i)
    car.orientedCarImg = pygame.transform.rotate(carImg, 90)
    cars.append(car)


pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("Racing")
clock = pygame.time.Clock()

gameIsOn = True

x = 350
y = 150
orientation = 90
acceleration = 0

# CHECKPOINTS
pygame.draw.rect(bg,(0,0,255), (310,130, 20,80))    # center (320,170)
pygame.draw.rect(bg,(0,0,254), (270,430, 20,80))    # center (280,470)
nextCheckpoint = 2
timeRace = time.time()

lastPixel = bg.get_at((int(x),int(y)))

bests, means, nbrIndiv = [], [], []

for gen in range(NB_GENERATION):
    print("Gen " + str(gen))
    timeCurrent = time.time()

    while(time.time() - timeCurrent < TIME_RACE):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()

        gameDisplay.blit(bg, (0,0))
        for car in cars:
            if(not car.alive):
                continue

            if(car.acceleration > 0):
                car.acceleration -= min(0.5, car.acceleration)
            
            if(car.x >= 0 and car.x < 800 and car.y >= 0 and car.y < 600):
                if(bg.get_at((int(car.x),int(car.y))) == (181, 230, 29, 255)):
                    if(lastPixel != bg.get_at((int(car.x),int(car.y)))):
                        car.acceleration/=3
                        car.alive = False
                    car.acceleration -= min(0.45, car.acceleration)
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
            dist = 0
            if(int(car.x+dx*50) >= 0 and int(car.x+dx*50) < 800 and int(car.y+dy*50) >= 0 and int(car.y+dy*50) < 600):
                if(bg.get_at((int(car.x+dx*50),int(car.y+dy*50))) == (181, 230, 29, 255)):
                    while(bg.get_at((int(car.x+dx*dist),int(car.y+dy*dist))) == (181, 230, 29, 255)):
                        dist+=1
                        if(dist==50):
                            break
                    pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx*50,car.y+dy*50))
                else : 
                    pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx*50,car.y+dy*50))

            car.totalDistance += car.acceleration
            car.x += dx*car.acceleration
            car.y += dy*car.acceleration
            if(car.x < 0 or car.x >= 800 or car.y < 0 or car.y >= 600):
                car.x -= dx*car.acceleration
                car.y -= dy*car.acceleration

            gameDisplay.blit(car.orientedCarImg, new_rect.topleft)
            gameDisplay.blit(lineSurface, (0,0))

            listInput = car.nn.evaluate([acceleration, dist])
            if(listInput[0] >= THRESHOLD):
                car.orientation -= 5

            if(listInput[1] >= THRESHOLD):
                car.orientation += 5

            if(listInput[2] >= THRESHOLD):
                car.acceleration += 1

            if(listInput[3] >= THRESHOLD):
                car.acceleration -= 0.5

        pygame.display.update()
        clock.tick(30)

    # Mandatory (before evolve)
    ga.fitness(cars)
    # <Display only>
    temp_results = ga.evaluate(cars)
    bests.append(temp_results[0])
    means.append(temp_results[1])
    nbrIndiv.append(len(cars))
    # </Display only>
    ga.evolve(cars)

X = [x for x in range(NB_GENERATION)]
ax1 = plt.subplot(211)
ax1.plot(X, bests, label="Bests")
ax1.plot(X, means, label="Means")
ax1.legend()
ax1.grid()
ax1.set_title("Performances")
ax2 = plt.subplot(224)
ax2.plot(X, nbrIndiv)
ax2.set_title("Nbr of individuals")
plt.show()