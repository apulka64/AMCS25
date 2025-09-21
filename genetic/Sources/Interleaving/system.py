from Interleaving.thread import *
from Interleaving.interleaving import *
from Interleaving.simpleOpt import *
import subprocess

class system:

    def __init__(self,fsys,minindistance):
        self.fsys = fsys
        self.indistance = minindistance
        self.threadList = list()
        self.interleaveRegister = interleavingReg(0)
        self.tfiSum = 0
        self.freqmargin = 0
        self.minFsys = 0



    def addThread(self,thread):
        self.threadList.append(thread)

    def setInterleavingWordSize(self,wordSize):
        self.interleaveRegister.setSize(wordSize)

    def calculateMinAppCountForThreads(self):

        self.tfiSum = 0

        #calculate sum of all TFi parameters for system
        for thread in self.threadList:
            self.tfiSum += float(thread.tfi.replace(',','.'))


        #calculate margin
        self.freqmargin = float(self.fsys) - self.tfiSum

        #derive minimal count of thread appearances in interleave register
        for thread in self.threadList:
            thread.calculateMinAppCount(self.tfiSum,self.interleaveRegister.wordSize)

    def calculateMinFreq(self):
        minSysFreqPerThread = list()

        for thread in self.threadList:
            thread.addActualOccurences(self.interleaveRegister.getThreadOccurenceCount(thread.id))
            thread.calculateMinSysF(self.interleaveRegister)
            minSysFreqPerThread.append(thread.minSysF)

        self.minFsys = max(minSysFreqPerThread)
        return

    def preprocessInterleavingReg(self):
        self.interleaveRegister.preprocessConfigWithStronghardThreads(self.threadList)
        return






    def print(self,topLevelPath):
        self.calculateMinFreq()
        print()
        print("System frequency: " + self.fsys+" MHz")
        print("System Min indistance: " + self.indistance)
        print("System TFi sum: " + str(self.tfiSum)+" Mhz")
        print("System frequency margin: "+ str(self.freqmargin)+" Mhz")
        print("System min frequency: " + str(self.minFsys) + " Mhz")

        print()
        for thread in self.threadList:
            thread.print()

        #print(self.interleaveRegister.regConfig)

        simpleOptPrintIl(self.interleaveRegister)

        #result = subprocess.getoutput
        print(topLevelPath + "\TaskSimulator.exe"+ " taskpath="+os.getcwd()+"\\Input\\test.td.txt"+ " interpath="+os.getcwd()+"\ProportionalMethod\\test.il.txt")
        result = subprocess.check_output(topLevelPath + "\TaskSimulator.exe"+ " taskpath="+os.getcwd()+"\Input\\test.td.txt"+ " interpath="+os.getcwd()+"\ProportionalMethod\\test.il.txt guioff showminfreq")

        minimalFrequencyOfTheSystem = str(result.decode('UTF-8')).replace("MinFreq=","")
        print(minimalFrequencyOfTheSystem)

        pathToOutFile = os.path.join(os.getcwd(), "ProportionalMethod\\result.out")
        f = open(pathToOutFile, "w+")
        f.write("Derived min frequency: "+ str(float(minimalFrequencyOfTheSystem))+"\n")
        f.write("System Min indistance: " + self.indistance+"\n")
        f.write("System TFi sum: " + str(self.tfiSum)+" Mhz"+"\n")
        f.close

        result = subprocess.check_output(topLevelPath + "\TaskSimulator.exe"+ " taskpath="+os.getcwd()+"\Input\\test.td.txt"+ " interpath="+os.getcwd()+"\GeneticMethod\\test.il.txt guioff showminfreq")

        minimalFrequencyOfTheSystem = str(result.decode('UTF-8')).replace("MinFreq=","")

        pathToOutFile = os.path.join(os.getcwd(), "GeneticMethod\\result.out")
        f = open(pathToOutFile, "w+")
        f.write("Derived min frequency: "+ str(float(minimalFrequencyOfTheSystem))+"\n")
        f.write("System Min indistance: " + self.indistance+"\n")
        f.write("System TFi sum: " + str(self.tfiSum)+" Mhz"+"\n")
        f.close
