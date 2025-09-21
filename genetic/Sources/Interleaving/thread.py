class thread:
    def __init__(self, threadId, tfi, strongHard):
        self.id = threadId
        self.tfi = tfi
        self.strongHard = strongHard
        self.normalizedMinCount = 0
        self.ocurrenceCount = 0
        self.minSysF = 0
        self.Di = 300
        self.MaxTw = 0

    def print(self):
        print("   Thread ID: "+ self.id)
        print("   Thread TFi: " + self.tfi)
        print("   Thread Strong Hard Type: " + self.strongHard)
        print("   Thread Minimal Count: " + str(self.normalizedMinCount))
        print()

    def calculateMinAppCount(self,tfiSum,wordSize):
        numTfi = float(self.tfi.replace(',','.'))
        self.normalizedMinCount = (numTfi/tfiSum)*wordSize

    def addActualOccurences(self, ocurrenceCount):
        self.ocurrenceCount = ocurrenceCount

    def calculateMinSysF(self,interleavingRegister):

        cnt = 0
        #get MaxTW param:
        for i in range(len(3*interleavingRegister.regConfig)):
            if( (3*interleavingRegister.regConfig)[i] == self.id):
                if(cnt > self.MaxTw):
                    self.MaxTw = cnt
                cnt = 0
            else:
                cnt = cnt + 1


        if(self.ocurrenceCount == 0):
            self.minSysF = float("inf")
        else:
            self.minSysF = (float(self.tfi)/float(self.ocurrenceCount))*float(interleavingRegister.wordSize) +(4+self.MaxTw-1)/self.Di


