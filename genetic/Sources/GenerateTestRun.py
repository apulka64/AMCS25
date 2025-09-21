import sys
import os
import datetime
import pathlib
import numpy as np
import shutil
from Interleaving.runMethod import *

def help():
    return

def createTestRun():
    popSizeTab = [100]
    iterCounts = [300]
    inputList = ["minres"]
    #interleaveLen = [2880,2400,3456]
    interleaveLen = [2880]

    inputFolderPath = os.getcwd()
    parent = os.path.join(inputFolderPath, os.pardir)
    projectFolder = os.path.abspath(parent)

    topLevelPath = createTopFolder()
    for popSize in popSizeTab:
        for iterLen in iterCounts:
            for input in inputList:
                executeTest( popSize , iterLen , input , interleaveLen[inputList.index(input)] , projectFolder)

    return

def createTopFolder():
    #move to test folder
    os.chdir("..")
    os.chdir("TestOutput")

    #create folder with relevant name
    timestamp = datetime.datetime.now()
    folderPath = "testrun_"+timestamp.strftime("%Y_%m_%d_%H_%M_%S")

    #create folder
    os.mkdir(folderPath)

    #move inside the created folder
    os.chdir(folderPath)
    return folderPath

def executeTest(popSize,iterLen,inputName,interleaveLen,pathToProjectDir):
    #create test enviroment - prepare input and folder structure
    workingDirName = "_".join([ str(popSize) ,str(iterLen) , inputName])
    currpath = os.getcwd()
    print(pathToProjectDir+"/TestInput/"+inputName,currpath)
    shutil.copytree(pathToProjectDir+"\TestInput\\"+inputName,currpath+"\\"+workingDirName)
    workingDirectoryPath = currpath+"\\"+workingDirName
    os.chdir(workingDirectoryPath)

    #execute actual test
    calculateSimpleMethod(pathToProjectDir,workingDirectoryPath,interleaveLen,popSize,iterLen)
    os.chdir("..")

    return

if __name__ == '__main__':
    createTestRun()

