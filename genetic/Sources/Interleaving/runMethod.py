from Interleaving.interleaving import *
from Interleaving.systemImport import *
from Interleaving.simpleOpt import *
from Interleaving.geneticPickAlg import *

def calculateSimpleMethod(topLevelPath,inputPath,interleavingWordLen,popSize,iterCnt):
    system = importSystemFromTa(str(inputPath)+'/Input/test.ta.txt')


    system.setInterleavingWordSize(interleavingWordLen)

    system.calculateMinAppCountForThreads()


    system.preprocessInterleavingReg()
    updateInterleaveRegWithGenAlgo(system,topLevelPath,popSize,iterCnt)
    updateInterleaveRegWithSimpleAlgo(system)

    system.print(topLevelPath)
