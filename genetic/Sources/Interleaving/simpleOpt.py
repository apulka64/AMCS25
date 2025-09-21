import Interleaving.system
import os
import math

def updateInterleaveRegWithSimpleAlgo(systemDefinition):
    minIndistanceCheckTable = (3*systemDefinition.interleaveRegister.regConfig)[len(systemDefinition.interleaveRegister.regConfig)-int(systemDefinition.indistance):len(systemDefinition.interleaveRegister.regConfig)+int(systemDefinition.indistance)]
    #print("Interleave:\n" + str(minIndistanceCheckTable))

    threadListForOpt = list()
    occurrenceCounters = list()

    for thread in systemDefinition.threadList:
        if thread.strongHard == "1":
            threadExpectedOccCnt = 0
        else:
            threadExpectedOccCnt = math.ceil(thread.normalizedMinCount)
        threadId = thread.id
        threadListForOpt.append([threadId,threadExpectedOccCnt])
        occurrenceCounters.append([threadId,0])


    for i in range(systemDefinition.interleaveRegister.wordSize):

        #check if stronghard task is already used
        if(systemDefinition.interleaveRegister.regConfig[i] == "0"):
            threadIdx = getIndexOfHighestOccCntReq(threadListForOpt, systemDefinition.interleaveRegister.wordSize, minIndistanceCheckTable,occurrenceCounters)
            if(threadIdx != "None"):

                #print(minIndistanceCheckTable)
                #print(threadListForOpt[threadIdx][0])

                systemDefinition.interleaveRegister.regConfig[i] = threadListForOpt[threadIdx][0]
                occurrenceCounters[threadIdx][1] = occurrenceCounters[threadIdx][1]+1

            minIndistanceCheckTable = (3*systemDefinition.interleaveRegister.regConfig)[len(systemDefinition.interleaveRegister.regConfig)-int(systemDefinition.indistance)+i:len(systemDefinition.interleaveRegister.regConfig)+int(systemDefinition.indistance)+i]

    return


def getIndexOfHighestOccCntReq(threadList, interleaveLen, blacklist, occurrenceCounters):

    x = interleaveLen
    for i in range(len(threadList)):
        if(threadList[i][0] not in blacklist):

            #avoid division by 0
            if threadList[i][1] is not 0:
                #check if analysed thread has currently the proportionally lowest occurence count
                if( x > occurrenceCounters[i][1]/threadList[i][1]):
                    x = occurrenceCounters[i][1]/threadList[i][1]

    #get first matching element
    for i in range(len(threadList)):
        if(threadList[i][0] not in blacklist):
            # avoid division by 0
            if threadList[i][1] is not 0:
                if(x == occurrenceCounters[i][1]/threadList[i][1]):
                    return i
    return "None"
    #print(x)

def simpleOptPrintIl(interleavingReg):
    os.mkdir("ProportionalMethod")
    pathToOutFile = os.path.join(os.getcwd(),"ProportionalMethod\\test.il.txt")
    f = open(pathToOutFile,"w+")
    f.write(str(interleavingReg.wordSize)+"\n")

    for node in interleavingReg.regConfig:
        f.write(node+"\n")

    f.close()
    return
