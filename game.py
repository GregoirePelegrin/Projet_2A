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
NB_CAR = 400
NB_BEST_CAR = 10
NB_GENERATION = 50
TIME_RACE = 300

#pygame.init() # Long to charge
pygame.font.init()
gameDisplay = pygame.display.set_mode((1300,600))
pygame.display.set_caption("Racing")
myfont = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

carImg = pygame.image.load("imgs/car.png").convert_alpha()
carImgBlue = pygame.image.load("imgs/carBlue.png").convert_alpha()

ga = lga.GeneticAlgorithm(ni=NB_CAR)

cars = []
for i in range(NB_CAR):
    car = lg.Car(i)
    car.orientedCarImg = pygame.transform.rotate(carImg, 90)
    cars.append(car)

VIEW_MODE = True
VIEW_BESTS_MODE = False
PAUSE_MODE = False

finished = False

drawing = False
points = []

exterior = [(231, 67), (370, 57), (502, 59), (602, 81), (625, 99), (635, 132), (635, 165), (622, 214), (619, 243), (629, 274), (647, 305), (654, 343), (652, 363), (647, 382), (637, 402), (620, 426), (605, 452), (592, 473), (567, 485), (544, 490), (517, 490), (494, 486), (467, 478), (461, 471), (442, 465), (422, 463), (399, 473), (385, 487), (365, 508), (347, 528), (310, 548), (284, 552), (256, 554), (229, 548), (214, 534), (202, 514), (182, 502), (174, 490), (161, 462), (154, 442), (152, 415), (151, 383), (150, 352), (142, 337), (133, 318), (119, 302), (101, 282), (92, 258), (91, 233), (96, 210), (104, 182), (114, 161), (125, 135), (137, 110), (158, 91), (178, 79), (205, 72), (230, 68)]
pygame.draw.lines(gameDisplay, (255,255,255), False, exterior)
interior = [(303, 100), (345, 98), (392, 96), (442, 96), (479, 100), (514, 106), (550, 118), (567, 130), (571, 142), (574, 158), (570, 173), (567, 198), (564, 216), (565, 230), (570, 256), (576, 278), (581, 286), (587, 304), (593, 329), (598, 346), (598, 362), (594, 373), (582, 390), (574, 402), (561, 412), (538, 421), (515, 420), (492, 416), (466, 412), (453, 413), (431, 418), (409, 424), (394, 428), (370, 442), (353, 459), (334, 474), (294, 485), (269, 485), (253, 477), (239, 466), (230, 450), (222, 423), (215, 400), (212, 381), (202, 351), (194, 321), (180, 295), (166, 270), (154, 245), (154, 217), (159, 198), (168, 178), (184, 155), (202, 141), (225, 123), (243, 110), (275, 102), (302, 100), (302, 100)]
pygame.draw.lines(gameDisplay, (255,255,255), False, interior)

# Graphs
graph_bests = plt.figure(figsize=[4, 3])
ax = graph_bests.add_subplot(111)
bests = []
means = []
ax.plot(bests, "-b", label="Bests")
ax.plot(means, ":r", label="Means")
ax.legend()
ax.set_title("Fitness vs generations")
canvas = agg.FigureCanvasAgg(graph_bests)

# NN area
X_SIZE = 400
Y_SIZE = 250
TOP_LEFT_X = 880
TOP_LEFT_Y = 330

currentBest = 0
selection = None
nbVisibleCars = NB_CAR
gen = 0
while gen < NB_GENERATION and not finished :
    timeGen = time.time()
    print("Gen " + str(gen))

    timeRace = 0
    while timeRace < TIME_RACE:
        tokenStop = True

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_v :
                    # Activate / deactivate viewing
                    VIEW_MODE = not VIEW_MODE
                    if not VIEW_MODE :
                        for car in cars :
                            car.orientedCarImg = None
                if event.key == pygame.K_e :
                    # End simulation
                    gen = NB_GENERATION
                if event.key == pygame.K_b :
                    # Activate / deactivate view of best cars
                    VIEW_BESTS_MODE = not VIEW_BESTS_MODE
                if event.key == pygame.K_SPACE:
                    # Pause generation
                    PAUSE_MODE = not PAUSE_MODE

            if(event.type == pygame.MOUSEBUTTONDOWN):
                for car in cars :
                    if event.pos[0] < car.x + 5 and event.pos[0] > car.x - 5 and event.pos[1] < car.y + 5 and event.pos[1] > car.y - 5 :
                        # print("clicked on car {}".format(car.id))
                        if selection is not None : selection.selected = False
                        car.selected = True
                        selection = car
                # Below for debugging
                #points.append(event.pos)
                #drawing = True
        
        ######## Testing intersection by mouse (needs VIEW_MODE = False)
        if drawing and len(points) > 1:
            gameDisplay.fill((0,0,0))
            pygame.draw.lines(gameDisplay, (255,255,255), False, interior)
            pygame.draw.lines(gameDisplay, (255,255,255), False, exterior)
            points[-1] = pygame.mouse.get_pos()
            r = None
            for p in range(len(interior)-1):
                r = cd.calculateIntersectPoint([points[-2][0], points[-2][1]], [points[-1][0], points[-1][1]],
                                        [interior[p][0], interior[p][1]], [interior[p+1][0], interior[p+1][1]])
                if r is not None :
                    pygame.draw.lines(gameDisplay, (255,0,0), False, points[-2:])
                    pygame.draw.circle(gameDisplay,(255,0,0),(r[0], r[1]), 2)
                    break
            if r is None :
                for p in range(len(exterior)-1):
                    r = cd.calculateIntersectPoint([points[-2][0], points[-2][1]], [points[-1][0], points[-1][1]],
                                            [exterior[p][0], exterior[p][1]], [exterior[p+1][0], exterior[p+1][1]])
                    if r is not None :
                        pygame.draw.lines(gameDisplay, (255,0,0), False, points[-2:])
                        pygame.draw.circle(gameDisplay,(255,0,0),(r[0], r[1]), 2)
                        break
            if r is None:
                pygame.draw.lines(gameDisplay, (0,255,0), False, points[-2:])
        ########

        ######## Set cars visibility
        if VIEW_BESTS_MODE:
            cars = sorted(cars, key=lambda x: x.totalDistanceLast, reverse=True)
            nbVisibleCars = NB_BEST_CAR
            for car in cars[NB_BEST_CAR:]:
                car.orientedCarImg = None
                car.visible = False
        else :
            nbVisibleCars = NB_CAR
            for car in cars :
                car.visible = True

        gameDisplay.fill((0,0,0), (0,0,800,600))
        gameDisplay.fill((0,0,0), (TOP_LEFT_X-10,TOP_LEFT_Y-10,TOP_LEFT_X+X_SIZE,TOP_LEFT_Y+Y_SIZE))
        pygame.draw.lines(gameDisplay, (255,255,255), False, interior)
        pygame.draw.lines(gameDisplay, (255,255,255), False, exterior)

        ######## Show numbers / modes
        textsurface = []
        textsurface.append(myfont.render("[B] Cars : {} ({} shown)".format(NB_CAR, nbVisibleCars), False, (255, 255, 255)))
        textsurface.append(myfont.render("Gen : {}".format(gen), False, (255, 255, 255)))
        textsurface.append(myfont.render("Best : {}".format(currentBest), False, (255, 255, 255)))
        if not VIEW_MODE :
            textsurface.append(myfont.render("[V] Viewing off", False, (255, 255, 255)))
        else :
            textsurface.append(myfont.render("[V] Viewing on", False, (255, 255, 255)))
        if PAUSE_MODE :
            textsurface.append(myfont.render("[SPACE] Game paused", False, (255, 255, 255)))
        else :
            textsurface.append(myfont.render("", False, (255, 255, 255)))
        for line in range(len(textsurface)) :
            if line == len(textsurface)-1 : # pause :
                gameDisplay.blit(textsurface[line],(600, 20))
            else :
                gameDisplay.blit(textsurface[line],(0,line*20))

        # for car in range(len(cars)):
        #     if cars[car].selected :
        #         cars.append(cars[car].copy())
        #         del cars[car]
            
        for car in cars :
            if(not car.alive):
                continue

            ######## Drawing  and views calculations
            if VIEW_MODE and car.visible :
                if not car.selected : car.orientedCarImg = pygame.transform.rotate(carImg, -car.orientation)
                else : car.orientedCarImg = pygame.transform.rotate(carImgBlue, -car.orientation)
                new_rect = car.orientedCarImg.get_rect(center = (car.x,car.y))

                lineSurface = pygame.Surface((800,600), pygame.SRCALPHA, 32)
                lineSurface = lineSurface.convert_alpha()
            
            
            ######## Show selected car's attributes / NN
            if car.selected :
                i = 0
                nb_layers = len(car.nn.layers)
                for layer in car.nn.layers :
                    j = 0
                    nb_neurons = len(layer.neurons)
                    for neuron in layer.neurons :
                        k = 0
                        nb_weights = len(neuron.weights)
                        for weight in neuron.weights :
                            pygame.draw.line(gameDisplay, (255,255,255),(TOP_LEFT_X+(i-1)*(X_SIZE/nb_layers), TOP_LEFT_Y+(Y_SIZE/nb_weights)/2+k*(Y_SIZE/nb_weights)),
                                                                        (TOP_LEFT_X+i*(X_SIZE/nb_layers), TOP_LEFT_Y+(Y_SIZE/nb_neurons)/2+j*(Y_SIZE/nb_neurons)))
                            k += 1
                        if i > 0 : # if not first layer
                            pygame.draw.circle(gameDisplay, (255,255-neuron.value*255,255-neuron.value*255), (TOP_LEFT_X+i*(X_SIZE/nb_layers), TOP_LEFT_Y+(Y_SIZE/nb_neurons)/2+j*(Y_SIZE/nb_neurons)), 7)

                        else : # if first layer
                            pygame.draw.circle(gameDisplay, (255,neuron.value*255/50,neuron.value*255/50), (TOP_LEFT_X+i*(X_SIZE/nb_layers), TOP_LEFT_Y+(Y_SIZE/nb_neurons)/2+j*(Y_SIZE/nb_neurons)), 7)

                        j+=1
                    i+=1


            VIEW_MODE and car.visible and gameDisplay.blit(car.orientedCarImg, new_rect.topleft)

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
            if(dist1 < 10 or dist2 < 10 or dist3 < 10):
                car.alive = False
                continue

            if dist1 < 50 :
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx1*50,car.y+dy1*50))
            else:
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx1*50,car.y+dy1*50))
            if dist2 < 50 :
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx2*50,car.y+dy2*50))
            else:
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx2*50,car.y+dy2*50))
            if dist3 < 50 :
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (255,0,0),(car.x,car.y),(car.x+dx3*50,car.y+dy3*50))
            else:
                VIEW_MODE and car.visible and pygame.draw.line(lineSurface, (0,255,0),(car.x,car.y),(car.x+dx3*50,car.y+dy3*50))

            VIEW_MODE and car.visible and gameDisplay.blit(car.orientedCarImg, new_rect.topleft)
            VIEW_MODE and car.visible and gameDisplay.blit(lineSurface, (0,0))
            ########

            if not PAUSE_MODE :
                car.x += dx1*car.speed
                car.y += dy1*car.speed
                car.totalDistance += (dx1**2+dy1**2)**0.5

                ######## Neural network inputs
                listInput = car.nn.evaluate([dist2, dist1, dist3])
                #listInput = [random.uniform(0, 1),random.uniform(0, 1)]
                
                if(listInput[0] >= THRESHOLD):
                    car.orientation -= 5

                if(listInput[2] >= THRESHOLD):
                    car.orientation += 5
                #########

                if car.x != car.lastX or car.y != car.lastY:
                    tokenStop = False
                
            car.nn.fitness = car.fitness()
            
        if tokenStop and not PAUSE_MODE:
            break
        if not PAUSE_MODE:
            timeRace += 1
        pygame.display.update()
        clock.tick(30)
    temp_data = ga.evolve([c.nn for c in cars])
    for car,nn in zip(cars, ga.nextGeneration):
        car.nn = nn
        car.selected = False
    cars[0].selected = True

    bestDist = 0
    sumTotal = 0
    for car in cars :
        sumTotal += car.totalDistance
        bestDist = max(bestDist, car.totalDistance)
        car.reinitialization()

    currentBest = bestDist
    bests.append(bestDist)
    means.append(sumTotal/len(cars))
    t = time.time()-timeGen
    if t != 0 :
        print("Time gen: " + str(round(t,1)) + "s / " + str(round(timeRace / t,1)) + " fps; bestDist: " + str(bestDist))
    
    # graphs
    ax.plot(bests, "-b", label="Bests")
    ax.plot(means, ":r", label="Means")
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surface_graph = pygame.image.fromstring(raw_data, size, "RGB")
    gameDisplay.blit(surface_graph,(850, 10))

    gen += 1

print(points)