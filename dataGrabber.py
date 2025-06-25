import os
from pathlib import Path
from datetime import datetime
import time
import csv
import pandas as pd

with open("cfg.txt") as cfgFile:
    KvPath = (cfgFile.read())

firstRun = False

dataPath = ("Data/")
dataFiles = os.listdir(dataPath)

#take first snapshot
previousFiles = set(os.listdir(KvPath))

def delete_all_files(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            os.remove(path)

def createCopyOfLastScenario(filepath):

    df = pd.read_csv(filepath)
    copyPath = "lastScenario/filepath.csv"
    df.to_csv(copyPath, index=False)

def getAverageScore(filepath):

    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    score = 0
    highScore = 0

    for index, row in df.iterrows():

        current_score = float(row["Score"])

        if highScore < float(row["Score"]):
            highScore = float(row["Score"])                  
            highScore = float(row["Score"])

        score += float(row["Score"])
   
    highScore = round((highScore),2)

    averageScore = round((score/len(df)),2)

    averageScoreHardGoal = round(averageScore + averageScore * (10 / 100),2)
    averageScoreSoftGoal = round(averageScore + averageScore * (5 / 100),2)

    print("HighScore: " + str(highScore))
    print("AverageScore: " + str(averageScore))
    print("SoftGoal: " + str(averageScoreSoftGoal))
    print("HardGoal: " + str(averageScoreHardGoal))


def findDataFile(Scenario):

    dataFiles = os.listdir(dataPath)
    fileName = (Scenario + ".csv")

    for file in dataFiles:
        if fileName == file:
            return fileName

def createNewFileAndAppendData(Scenario, Score, Accuracy,dateAndTime):

    print("Creating New file And Appending Data")

    with open(dataPath + "/" + Scenario + ".csv", "w") as f:   # Opens file and casts as f 
        f.write("Scenario, DateAndTime, Score, Accuracy")
        f.write("\n")
        f.write(Scenario + "," + dateAndTime + "," + str(Score) + "," + str(Accuracy))

def createAndAppendDataFiles(Scenario, Score, Accuracy,dateAndTime):

    dataFiles = os.listdir(dataPath)  

    if len(dataFiles) == 0:

        createNewFileAndAppendData(Scenario, Score, Accuracy, dateAndTime)

    else:
    
        found = False

        for file in dataFiles:
            if (Scenario + ".csv") == file:
                found = True
                print("Appending Data")
                with open(dataPath + "/" + Scenario + ".csv", "a") as f:
                    f.write("\n")
                    f.write(Scenario + "," + dateAndTime + "," + str(Score) + "," + str(Accuracy))
                break

        if found == False:
                
            createNewFileAndAppendData(Scenario, Score, Accuracy, dateAndTime)
    

def readFromNewFile(newfile):

    timestamp = os.path.getctime(KvPath +  '/' + newfile)
    dateAndTime = datetime.fromtimestamp(timestamp).strftime("%Y.%m.%d-%H.%M")

    with open(KvPath +  '/' + newfile, 'r') as csv_file:

        csv_reader = csv.reader(csv_file)
        for line in csv_reader:

            if len(line) >= 2:
                 
                 if line[0] == "Scenario:":
                     Scenario = (line[1])
                
                 elif line[0] == "Score:":
                     Score = float(line[1])

                 elif line[0] == "Hit Count:":
                     hits = int(line[1])

                 elif line[0] == "Miss Count:":
                      misses = int(line[1])
    
    Accuracy = round((hits / (hits + misses)) * 100, 2)

    os.system('cls')

    createAndAppendDataFiles(Scenario, Score, Accuracy, dateAndTime)

    if firstRun == False:
        
        print("--------------------------------")
        print("Scenario: " + Scenario)
        print("Date And Time: " + dateAndTime)
        print("Accuracy: " + str(Accuracy) + "%")
        print("Score: " + str(Score))
        filePath = (dataPath + (findDataFile(Scenario)))
        getAverageScore(filePath)
        delete_all_files("lastScenario")
        createCopyOfLastScenario(filePath)
  
 

def readFromFiles():

    global firstRun

    for file in previousFiles:
        readFromNewFile(file)
    firstRun = False
    print("all data has been collected")
    

print("Scanning Files")

if (len(dataFiles)) == 0:
     firstRun = True
     print("found no data files in your data folder, creating new data files")
     readFromFiles()

    
while True:

    #second snapshot
    currentFiles = set(os.listdir(KvPath))

    if (currentFiles.difference(previousFiles)):

        newfiles = (currentFiles.difference(previousFiles))
        newfile = newfiles.pop()

        readFromNewFile(newfile)
       
        previousFiles = currentFiles
    
    time.sleep(2)
