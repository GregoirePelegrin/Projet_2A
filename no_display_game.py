import pygame
import os
import math
import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

import Libraries.LibraryGeneticAlgorithm as lga
import Libraries.LibraryGame as lg
import Libraries.collisionDetection as cd

THRESHOLD = 0.55
NB_CAR = 200
NB_BEST_CAR = 10
NB_GENERATION = 500
TIME_RACE = 300

ga = lga.GeneticAlgorithm(ni=NB_CAR)

cars = []
for i in range(NB_CAR):
    car = lg.Car(i)
    cars.append(car)

finished = False

exterior = [(231, 67), (370, 57), (502, 59), (602, 81), (625, 99), (635, 132), (635, 165), (622, 214), (619, 243), (629, 274), (647, 305), (654, 343), (652, 363), (647, 382), (637, 402), (620, 426), (605, 452), (592, 473), (567, 485), (544, 490), (517, 490), (494, 486), (467, 478), (461, 471), (442, 465), (422, 463), (399, 473), (385, 487), (365, 508), (347, 528), (310, 548), (284, 552), (256, 554), (229, 548), (214, 534), (202, 514), (182, 502), (174, 490), (161, 462), (154, 442), (152, 415), (151, 383), (150, 352), (142, 337), (133, 318), (119, 302), (101, 282), (92, 258), (91, 233), (96, 210), (104, 182), (114, 161), (125, 135), (137, 110), (158, 91), (178, 79), (205, 72), (230, 68)]
interior = [(303, 100), (345, 98), (392, 96), (442, 96), (479, 100), (514, 106), (550, 118), (567, 130), (571, 142), (574, 158), (570, 173), (567, 198), (564, 216), (565, 230), (570, 256), (576, 278), (581, 286), (587, 304), (593, 329), (598, 346), (598, 362), (594, 373), (582, 390), (574, 402), (561, 412), (538, 421), (515, 420), (492, 416), (466, 412), (453, 413), (431, 418), (409, 424), (394, 428), (370, 442), (353, 459), (334, 474), (294, 485), (269, 485), (253, 477), (239, 466), (230, 450), (222, 423), (215, 400), (212, 381), (202, 351), (194, 321), (180, 295), (166, 270), (154, 245), (154, 217), (159, 198), (168, 178), (184, 155), (202, 141), (225, 123), (243, 110), (275, 102), (302, 100), (302, 100)]
checkpoints = [[(408, 58), (408, 98)], [(487, 60), (475, 99)], [(575, 74), (547, 117)], [(632, 127), (572, 139)], [(627, 187), (571, 175)], [(619, 228), (564, 225)], [(632, 279), (584, 298)], [(654, 348), (598, 343)], [(632, 410), (590, 385)], [(551, 488), (523, 422)], [(453, 470), (455, 414)], [(394, 476), (367, 447)], [(340, 524), (312, 479)], [(203, 517), (238, 470)], [(219, 412), (152, 422)], [(150, 352), (195, 329)], [(165, 268), (97, 273)], [(155, 203), (109, 172)], [(203, 143), (164, 84)], [(263, 102), (257, 66)]]

X_SIZE = 400
Y_SIZE = 250
TOP_LEFT_X = 880
TOP_LEFT_Y = 330

gen = 0
while gen < NB_GENERATION and not finished :
    timeGen = time.time()
    print("Gen " + str(gen))
    
    timeRace = 0
    while timeRace < TIME_RACE:
        tokenStop = True
            
        for car in cars :
            if(not car.alive):
                continue
            
            dx1 = math.cos((car.orientation-90) * math.pi / 180)
            dy1 = math.sin((car.orientation-90) * math.pi / 180)
            dx2 = math.cos((car.orientation-45) * math.pi / 180)
            dy2 = math.sin((car.orientation-45) * math.pi / 180)
            dx3 = math.cos((car.orientation-135) * math.pi / 180)
            dy3 = math.sin((car.orientation-135) * math.pi / 180)

            dist1 = None
            dist2 = None
            dist3 = None
            for p in range(len(interior)-1):
                if dist1 is None :
                    dist1 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx1*50,car.y+dy1*50],
                                            interior[p], interior[p+1])
                if dist2 is None :
                    dist2 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx2*50,car.y+dy2*50],
                                        [interior[p][0], interior[p][1]], [interior[p+1][0], interior[p+1][1]])
                if dist3 is None :
                    dist3 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx3*50,car.y+dy3*50],
                                        [interior[p][0], interior[p][1]], [interior[p+1][0], interior[p+1][1]])

            for p in range(len(exterior)-1):
                if dist1 is None :
                    dist1 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx1*50,car.y+dy1*50],
                                        [exterior[p][0], exterior[p][1]], [exterior[p+1][0], exterior[p+1][1]])
                if dist2 is None :
                    dist2 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx2*50,car.y+dy2*50],
                                        [exterior[p][0], exterior[p][1]], [exterior[p+1][0], exterior[p+1][1]])
                if dist3 is None :
                    dist3 = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx3*50,car.y+dy3*50],
                                        [exterior[p][0], exterior[p][1]], [exterior[p+1][0], exterior[p+1][1]])

            if dist1 is None :
                dist1 = 50
            else :
                dist1 = math.sqrt( (car.x-dist1[0])**2 + (car.y-dist1[1])**2 )
            if dist2 is None :
                dist2 = 50
            else :
                dist2 = math.sqrt( (car.x-dist2[0])**2 + (car.y-dist2[1])**2 )
            if dist3 is None :
                dist3 = 50
            else :
                dist3 = math.sqrt( (car.x-dist3[0])**2 + (car.y-dist3[1])**2 )
            if(dist1 < 11 or dist2 < 11 or dist3 < 11):
                car.alive = False
                continue
            
            # Check checkpoints
            for p in range(len(checkpoints)-1):
                dist = cd.calculateIntersectPoint([car.x, car.y], [car.x+dx1*50,car.y+dy1*50],
                                        checkpoints[p][0], checkpoints[p][1])
                if dist is not None :
                    dist = math.sqrt( (car.x-dist[0])**2 + (car.y-dist[1])**2 )
                    if dist < 11 and p == car.nextCheckpointId :
                        car.nextCheckpointId += 1
            
            car.x += dx1*car.speed
            car.y += dy1*car.speed
            car.totalDistance = car.nextCheckpointId - 1

            ######## Neural network inputs
            speed_normalized = (car.speed +5) / 15
            dist1_normalized = dist1 / 50
            dist2_normalized = dist2 / 50
            dist3_normalized = dist3 / 50
            listInput = car.nn.evaluate([speed_normalized, dist2_normalized, dist1_normalized, dist3_normalized])
            #listInput = [random.uniform(0, 1),random.uniform(0, 1)]
            
            if(listInput[0] >= THRESHOLD):
                car.orientation -= 5

            if(listInput[1] >= THRESHOLD):
                if car.speed <= 10 :
                    car.speed += 1
            if(listInput[2] >= THRESHOLD):
                if car.speed >= -5 :
                    car.speed -= 1

            if(listInput[3] >= THRESHOLD):
                car.orientation += 5

        car.nn.fitness = car.fitness()
        timeRace += 1

    temp_data = ga.evolve([c.nn for c in cars])
    for car,nn in zip(cars, ga.nextGeneration):
        car.nn = nn
    
    bestDist = 0
    sumTotal = 0
    for car in cars :
        sumTotal += car.totalDistance
        bestDist = max(bestDist, car.totalDistance)
        car.reinitialization()

    t = time.time()-timeGen
    if t != 0 :
        print("Time gen: " + str(round(t,1)) + "s / " + str(round(timeRace / t,1)) + " fps; bestDist: " + str(bestDist))
    
    gen += 1