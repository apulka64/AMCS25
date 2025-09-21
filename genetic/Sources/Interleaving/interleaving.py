import math



class interleavingReg:

    def __init__(self,size):
        self.wordSize = size
        self.regConfig = list()
        print(self.regConfig , self.wordSize)

    def setSize(self, size):
        self.wordSize = size

    def setNextThreadId(self,threadId):
        self.regConfig.append(threadId)

    def setThreadList(self,threadList):
        self.regConfig = threadList

    def getThreadOccurenceCount(self,threadId):
        return self.regConfig.count(threadId)

    def preprocessConfigWithStronghardThreads(self,threadList):

        #initialize reg config with 0 thread
        for i in range(0,self.wordSize):
            self.regConfig.append("0")

        for thread in threadList:
            if thread.strongHard == "1" :
                ShtTask = thread.id
                #calculate window size for SHT task - shall be an integer, cannot be higher than calculated value - rounded to lowest number
                windowSize = math.floor(self.wordSize/thread.normalizedMinCount)


        #set SHT task
        for i in range(0,self.wordSize,windowSize):
            self.regConfig[i] = ShtTask

        print(self.regConfig)

        return


