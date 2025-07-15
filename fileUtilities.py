import os
from datetime import datetime
import time
import shutil
import pandas as pd


#reading data

def readFile(file):
    with open(file, "r") as file:
        content = file.read()
        return content
    
def readLines(file):
    lines = []
    with open(file, "r") as file:
        for line in file:
            lines.append(line.rstrip())
    return lines

def getAttributes(file, target):
    lines = readLines(file)
    for line in lines:
        if target in line:
            return(line.split(',',1)[1])
        
def getDateTime(file):
    timestamp = os.path.getctime(file)
    dateAndTime = datetime.fromtimestamp(timestamp).strftime("%Y.%m.%d-%H.%M")
    return dateAndTime

def getFilesInDirectory(path):
    files = os.listdir(path)
    return files

#writing data

def deleteFilesInDirectory(path):

    for file in os.listdir(path):                   
        os.remove(os.path.join(path, file))

def appendData(fileName ,path, content):
    with open(path + "/" + fileName, "a") as file:
        file.write(content + "\n")

def createFile(fileName, path):
    with open(path + "/" + fileName, "x") as file:
        file.close()

#Searching Data
   
def findFileInDirectory(fileName, path):
     
    found = False
    files = getFilesInDirectory(path)
    for file in files:
        if fileName == file:
            found = True
            return found
        
    return found

def isADirectory(path):
    if os.path.exists(path):
        return True
    else:
        return False
    
def getDifference(currentSnapshot, previousSnapshot):
    difference = currentSnapshot.difference(previousSnapshot)
    if difference:
        return difference.pop()

#copying data

def copyCsvFile(source, destination):
    shutil.copy(source, destination)

#Miscellaneous

def clear_console():
    os.system('cls')

def getAverageScoreFromCSV(file):
    df = pd.read_csv(file)
    averageScore = round(df['Score'].mean(),2)
    return averageScore

def getHighestScoreFromCSV(file):
    df = pd.read_csv(file)
    highestScore = round(df['Score'].max(),2)
    return highestScore

    
    








   

       
    
    





