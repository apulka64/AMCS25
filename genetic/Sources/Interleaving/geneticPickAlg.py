import random
import os
import subprocess
import shutil
import time
import sys
import string
import asyncio
import shlex
import numpy as np
import math


POP_SIZE = 300
ITER_COUNT = 30
CROSSOVER_POINTS = 3
MUTATION_SIZE = 50
MUTATION_COUNT = 1
ELITE_PERCENTAGE = 0.05
CULL_PERCENTAGE = 0.25
NEW_POPS_PERCENTAGE = 0

def updateInterleaveRegWithGenAlgo(systemDefinition,topLevelPath,popSize,iterCnt):
    os.mkdir("GeneticMethod")
    global POP_SIZE
    POP_SIZE = popSize
    global ITER_COUNT
    ITER_COUNT = iterCnt

    updatedThreadList = systemDefinition.threadList



    for thread in systemDefinition.threadList:
        if thread.strongHard is "1":
            updatedThreadList.remove(thread)

    #preconfigure interleaving config pop - skip stronghard tasks
    print(str(time.asctime()) + " Initial population generation start ")
    print("Interleave register width: ",systemDefinition.interleaveRegister.wordSize)
    print("Expected pop count:",POP_SIZE)
    print("Expected iterations:", ITER_COUNT)
    print("Crossover points: ", CROSSOVER_POINTS)
    print("Mutation points: ", MUTATION_COUNT)
    print("Mutation size: ", MUTATION_SIZE)
    print("Elite percentage: ", ELITE_PERCENTAGE*100,"%")
    print("Cull percentage: ", CULL_PERCENTAGE*100,"%")
    print("New pop percentage: ", NEW_POPS_PERCENTAGE*100,"%")
    pathToConfigInfo = os.path.join(os.getcwd(), "GeneticMethod\\configuration.txt")
    configInfo = open(pathToConfigInfo, "w+")
    configInfo.write("Interleave register width: "+ str(systemDefinition.interleaveRegister.wordSize)+"\n")
    configInfo.write("Expected pop count:"+str(POP_SIZE)+"\n")
    configInfo.write("Expected iterations:"+str(ITER_COUNT)+"\n")
    configInfo.write("Crossover points: "+str(CROSSOVER_POINTS)+"\n")
    configInfo.write("Mutation points: "+str(MUTATION_COUNT)+"\n")
    configInfo.write("Mutation size: "+str(MUTATION_SIZE)+"\n")
    configInfo.write("Elite percentage: "+str(ELITE_PERCENTAGE*100)+"%\n")
    configInfo.write("Cull percentage: "+str(CULL_PERCENTAGE*100)+"%\n")
    configInfo.write("New pop percentage: " + str(NEW_POPS_PERCENTAGE * 100) + "%\n")
    configInfo.close()

    population = initializePop(systemDefinition.interleaveRegister.regConfig, systemDefinition.interleaveRegister.wordSize, updatedThreadList, POP_SIZE, systemDefinition.indistance)
    print(str(time.asctime()) + " Initial population generation end ")

    pathToIterInfoFile = os.path.join(os.getcwd(), "GeneticMethod\\iterations.csv")
    iterInfoFile = open(pathToIterInfoFile, "w+")
    iterInfoFile.write("IterCnt;BestFitness;AvgFitness\n")



    for count in range(ITER_COUNT):
        print(str(time.asctime()) + " Process start ")
        print("Progress: "+str((count/ITER_COUNT)*100)+"%")
        startTime = time.time()
        fitnessTab = [0]*POP_SIZE
        fitnessSum = 0


        fitnessTab = calculateFitness(topLevelPath, systemDefinition, population)
        fitnessSum = sum(fitnessTab)
        avgFitness = fitnessSum / POP_SIZE

        iterInfoFile.write( ";".join( [ str(count), str(max(fitnessTab)) , str(avgFitness) ] ).replace(".",",") + "\n" )

        endTime = time.time()
        print(str(time.asctime())+" Fitness calc time: "+ str(endTime-startTime))

        print(fitnessTab)
        print(len(fitnessTab))
        print(fitnessSum)

        startTime = time.time()
        children = list()
        sortedPops, sortedFitness = selectParents(population,fitnessTab)
        parents = sortedPops[:math.floor((len(sortedPops))*(1-CULL_PERCENTAGE))]
        parentFitness = sortedFitness[:math.floor(len(sortedFitness)*(1-CULL_PERCENTAGE))]

        #add elite to childs
        children = sortedPops[:math.ceil(POP_SIZE *(ELITE_PERCENTAGE))]

        for i in range(POP_SIZE - (math.floor( POP_SIZE * ELITE_PERCENTAGE) + math.floor(POP_SIZE*NEW_POPS_PERCENTAGE)) ):
            child = crossover(parents,parentFitness,updatedThreadList,systemDefinition.interleaveRegister.wordSize,systemDefinition.indistance)
            children.append(child)

        regenPops = initializePop(systemDefinition.interleaveRegister.regConfig, systemDefinition.interleaveRegister.wordSize, updatedThreadList, math.ceil(POP_SIZE*NEW_POPS_PERCENTAGE), systemDefinition.indistance)
        children = children + regenPops

        endTime = time.time()
        print(str(time.asctime())+" Children calc time: " + str(endTime - startTime))
        startTime = time.time()
        population = children[:]
        endTime = time.time()
        print(str(time.asctime()) + " Post process calc time: " + str(endTime - startTime))
        print()
        print()

    iterInfoFile.close()





    pathToOutFile = os.path.join(os.getcwd(), "GeneticMethod\\test.il.txt")
    f = open(pathToOutFile, "w+")
    f.write(str(systemDefinition.interleaveRegister.wordSize) + "\n")

    for node in population[fitnessTab.index(max(fitnessTab))]:
        f.write(node + "\n")

    f.close()



    return

def initializePop(interleaveConfig,interleaveLen,threadList, popSize,minIndistance):

    population = list()
    weights = list()

    minIndistanceCheckTable = (3 * interleaveConfig)[len(interleaveConfig) - int(minIndistance):len(interleaveConfig)]

    for thread in threadList:
        weights.append(thread.normalizedMinCount)

    for k in range(popSize):

        #init pop with interleave configuration
        pop = interleaveConfig[:]
        for i in range(interleaveLen):
            if interleaveConfig[i] is "0":
                pop[i] = random.choices(threadList,weights,k=1)[0].id
                while pop[i] in minIndistanceCheckTable:
                    pop[i] = random.choices(threadList, weights, k=1)[0].id
            minIndistanceCheckTable = (3 * pop)[len(interleaveConfig) - int(minIndistance)+i:len(interleaveConfig)+i]
        population.append(pop)

    return population

def calculateFitness(topLevelPath,systemDefinition,population):

    fitnessList = list()
    os.mkdir("temp")

    listOfIlFiles = list()

    for pop in population:
        listOfIlFiles.append(printIlToFile(topLevelPath,systemDefinition,pop,population.index(pop)))

    processList = list()
    for pop in population:
        with open(os.getcwd() + "\\temp\\"+listOfIlFiles[population.index(pop)]+".result","w+") as outFile:
            process = subprocess.Popen( (topLevelPath + "\TaskSimulator.exe" + " taskpath=" + os.getcwd() + "\Input\\test.td.txt" + " interpath=" + os.getcwd() + "\\temp\\"+listOfIlFiles[population.index(pop)]+".il.txt guioff showminfreq").split(),shell=False,stdout=outFile,stderr=outFile)
            processList.append(process)
        outFile.close()

    for p in processList:
        p.wait()

    for pop in population:
        with open(os.getcwd() + "\\temp\\" + listOfIlFiles[population.index(pop)] + ".result", "r") as outFile:

            callResult = outFile.read()
            #print("ReadFile " + os.getcwd() + "\\temp\\" + listOfIlFiles[population.index(pop)] + ".result" + "w+")
            #print(outFile.read())
            #print(callResult.replace("MinFreq=", ""))
            calcMinFreq = float(callResult.replace("MinFreq=", ""))
            fitness = systemDefinition.tfiSum/calcMinFreq
            fitnessList.append(fitness)


    shutil.rmtree("temp")

    return fitnessList

def printIlToFile(topLevelPath,systemDefinition,pop,pos):
    interleave = pop[:]
    interleaveRegVal = preprocessInterleaveForGaps(interleave,systemDefinition.indistance)

    pathToOutFile = os.path.join(os.getcwd()+"\\temp\\"+str(pos)+".il.txt")
    #print(pathToOutFile)
    f = open(pathToOutFile,"w+")
    f.write(str(len(pop))+"\n")

    for node in interleaveRegVal:
        f.write(node+"\n")

    f.close()
    return str(pos)

def preprocessInterleaveForGaps(interleaveConfig,minIndistance):
    minIndistanceCheckTable = (2*interleaveConfig)[len(interleaveConfig)-int(minIndistance):len(interleaveConfig)]

    for i in range(len(interleaveConfig)):
        if interleaveConfig[i] in minIndistanceCheckTable :
            interleaveConfig[i] = "0"
        minIndistanceCheckTable = (2 * interleaveConfig)[len(interleaveConfig) - int(minIndistance) + i : len(interleaveConfig) + i ]

    return interleaveConfig



def crossover(pops, parentsFitnessTab, whitelist, wordSize,minIndistance):

    whitelistNames = list("0")

    for thread in whitelist:
        whitelistNames.append(thread.id)

    parents = random.choices(pops, weights = parentsFitnessTab , k = 2)

    childChromosomes = list()
    parentsChromosomes = list()
    child = list()

    crossoverPoints = sorted(random.sample(range(wordSize),CROSSOVER_POINTS))

    #pick parents and get parent chromosome list
    for parent in parents:
        parentsChromosomes.append(np.split(parent,crossoverPoints))

    #pick chromosomes from parents
    for i in range(CROSSOVER_POINTS+1):
        childChromosomes.append(parentsChromosomes[random.choice([0,1])][i])

    for chromosome in childChromosomes:
        child.extend(chromosome)

    #mutate genes
    for i in range(MUTATION_COUNT):
        #get start position of mutation
        mutationStartPos = random.randint(i*int(wordSize / MUTATION_COUNT), ((i+1)*int(wordSize / MUTATION_COUNT) - MUTATION_SIZE))

        #print("Mutation pos: ", mutationStartPos)
        #print("Old genes ", child[mutationStartPos:mutationStartPos + MUTATION_SIZE])
        #erase current valid genes
        for mutateGenPos in range(mutationStartPos,mutationStartPos + MUTATION_SIZE):
            if child[mutateGenPos] in whitelistNames:
                child[mutateGenPos] = "0"
        #print("Erased genes ", child[mutationStartPos:mutationStartPos + MUTATION_SIZE])
        for mutateGenPos in range(mutationStartPos,mutationStartPos + MUTATION_SIZE):
            #mutate gene - assure gene is correct -> would not end up in being a 0 and is not a SHT task
            if child[mutateGenPos] in whitelistNames:
                minIndistanceCheckTable = (3 * child)[len(child) - int(minIndistance) + mutateGenPos: len(child) + mutateGenPos]
                while True:
                    newGene = random.choice(whitelistNames)
                    if newGene not in minIndistanceCheckTable:
                        child[mutateGenPos] = newGene
                        break
        #print("Mutation pos: ",mutationStartPos)
        #print("New genes ", child[mutationStartPos:mutationStartPos+MUTATION_SIZE])



    return child

def selectParents(pop,fitness):
    zippedLists = zip( fitness, pop)
    sortedLists = sorted(zippedLists, reverse=True)

    tuples = zip(*sortedLists)
    fitnesses, pops = [list(tuple) for tuple in  tuples]
    print(fitnesses)
    return pops,fitness