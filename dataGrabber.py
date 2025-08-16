import fileUtilities as futils
import time
import sys

#Logo

logo = r"""
$$$$$$$\             $$\                      $$$$$$\                     $$\       $$\                           
$$  __$$\            $$ |                    $$  __$$\                    $$ |      $$ |                          
$$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\        $$ /  \__| $$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
$$ |  $$ | \____$$\\_$$  _|   \____$$\       $$ |$$$$\ $$  __$$\ \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$ |  $$ | $$$$$$$ | $$ |     $$$$$$$ |      $$ |\_$$ |$$ |  \__|$$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
$$ |  $$ |$$  __$$ | $$ |$$\ $$  __$$ |      $$ |  $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      
$$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$$$$ |      \$$$$$$  |$$ |     \$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      
\_______/  \_______|  \____/  \_______|       \______/ \__|      \_______|\_______/ \_______/  \_______|\__|      
"""

#Functions

def createAndApendDataFiles(file, dataPath, outPutPath, printLogo, copyFiles):

    Score = futils.getAttributes(file,"Score")
    Scenario = futils.getAttributes(file,"Scenario")
    hitCount = int(futils.getAttributes(file,"Hit Count"))
    missCount = int(futils.getAttributes(file,"Miss Count"))
    Accuracy = round((hitCount / (hitCount + missCount)) * 100, 2)
    dateAndTime = futils.getDateTime(file)
    fileName = (Scenario + ".csv")
    content = (str(Scenario) + "," + str(dateAndTime) + "," + str(Score) + "," + str(Accuracy))
    fileExist = futils.findFileInDirectory(fileName, dataPath)

    if fileExist == False:
        futils.createFile(fileName, dataPath)
        futils.appendDataPath(fileName, dataPath, "Scenario,DateAndTime,Score,Accuracy")
        futils.appendDataPath(fileName, dataPath, content)
    elif fileExist == True:
        futils.appendDataPath(fileName, dataPath, content)

    if printLogo == True:

        averageScore = futils.getAverageScoreFromCSV(dataPath + "/" + fileName)
        highestScore = futils.getHighestScoreFromCSV(dataPath + "/" + fileName)

        print(logo)
        print("-----------------------------------------------------------------------------------------------------------------------")
        print(f"{Scenario}\n{dateAndTime}\n\nHighScore: {highestScore}\nCurrent_Score: {Score}\nAverage_Score: {averageScore}\nAccuracy {Accuracy}%")

    if copyFiles == True:
        futils.deleteFilesInDirectory(outPutPath)
        futils.copyCsvFile((dataPath + "/" + fileName), outPutPath)

        
def init(kovaaksPath, dataPath, outPutPath, processedFiles):

    kovaaksFiles = futils.getFilesInDirectory(kovaaksPath)

    for file in kovaaksFiles: 
        hasBeenProcessed: bool = False

        lines = futils.readLines(processedFiles)
        for line in lines:
            if file == line:
                hasBeenProcessed = True

        if hasBeenProcessed == False:
            print("file has not been proccesed yet")
            futils.appendData(processedFiles, file)
            
            file = (kovaaksPath + "/" + file)
            createAndApendDataFiles(file, dataPath, outPutPath, False, False)
   
def hasRanBefore(dataPath):
    if len(futils.getFilesInDirectory(dataPath)) == 0:
        return False
    else:
        return True

#initialize variables

processedFiles = ("processedFiles.txt")
kovaaksPath = (futils.readFile("cfg.txt"))
dataPath = ("Data/")
outPutPath = ("Output/")
hasStarted = False
previousSnapshot = set(futils.getFilesInDirectory(kovaaksPath))

#main logic

if futils.isADirectory(kovaaksPath) == False:
    print("your kovaaks stats directory is incorrect please delete all the data in your cfg file and repaste your kovaaks directory")
    input()
    sys.exit()

if hasStarted == False:
    
    print(logo)
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("Collecting Data please wait until all your data is collected")
    init(kovaaksPath, dataPath, outPutPath, processedFiles)
    futils.clear_console()
    print(logo)
    print("All your data has been collected scanning for new files")
  

while True:

    currentSnapshot = set(futils.getFilesInDirectory(kovaaksPath))
    file = futils.getDifference(currentSnapshot, previousSnapshot)
    
    if file:
        futils.appendData(processedFiles, file)
        file = (kovaaksPath + "/" + file)
        futils.clear_console()
        createAndApendDataFiles(file, dataPath, outPutPath, True, True)
        previousSnapshot = currentSnapshot
        
    time.sleep (2)

input = input()
