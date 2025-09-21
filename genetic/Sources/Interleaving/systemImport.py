from Interleaving.system import *
from Interleaving.thread import *

def importSystemFromTa(importFile):

    with open(importFile) as f:
        lines = f.readlines()

    if "Fsys;FSmarg;Minindistance;WL" in lines[0]:
        systemParams = lines[1].split(";")

        #uses only system frequency(Fsys) and Minindistance
        importedSystem = system(systemParams[0],systemParams[2])
    else:
        raise Exception("Incorrect file format - expected correct .ta.txt file")

    if "ThID;TF;SHT;HM;TW" in lines[2]:
        print("Correct .ta.txt file format.")
    else:
        raise Exception("Incorrect file format - expected correct .ta.txt file")

    #extract lines with only thread params
    importThreadListTxt = lines[3:]

    for threadLine in importThreadListTxt:
        threadParams = threadLine.split(";")

        #import only Thread ID Thread TFi and Thread Strong Hard param
        addedThread = thread(threadParams[0],threadParams[1].replace(",","."),threadParams[2])
        importedSystem.addThread(addedThread)

    return importedSystem


