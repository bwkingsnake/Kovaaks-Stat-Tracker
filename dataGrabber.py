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
        futils.appendData(fileName, dataPath, "Scenario,DateAndTime,Score,Accuracy")
        futils.appendData(fileName, dataPath, content)

    elif fileExist == True:

        futils.appendData(fileName, dataPath, content)
    
    if printLogo == True:

        averageScore = futils.getAverageScoreFromCSV(dataPath + "/" + fileName)
        highestScore = futils.getHighestScoreFromCSV(dataPath + "/" + fileName)

        print(logo)
        print("-----------------------------------------------------------------------------------------------------------------------")
        print(f"{Scenario}\n{dateAndTime}\n\nHighScore: {highestScore}\nCurrent_Score: {Score}\nAverage_Score: {averageScore}\nAccuracy {Accuracy}%")

    if copyFiles == True:
        futils.deleteFilesInDirectory(outPutPath)
        futils.copyCsvFile((dataPath + "/" + fileName), outPutPath)

        
def init(kovaaksPath, dataPath, outPutPath):
    kovaaksFiles = futils.getFilesInDirectory(kovaaksPath)
    for file in kovaaksFiles:
        file = (kovaaksPath + "/" + file)
        createAndApendDataFiles(file, dataPath, outPutPath, False, False)

   
def hasRanBefore(dataPath):
    if len(futils.getFilesInDirectory(dataPath)) == 0:
        return False
    else:
        return True

#initialize variables

kovaaksPath = (futils.readFile("cfg.txt"))
dataPath = ("Data/")
outPutPath = ("Output/")
hasStarted = hasRanBefore(dataPath)
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
    init(kovaaksPath, dataPath, outPutPath)
    print("All your data has been collected")
    print("Scanning For New Files")
else:
    print(logo)
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("Scanning For New Files")


while True:

    currentSnapshot = set(futils.getFilesInDirectory(kovaaksPath))
    file = futils.getDifference(currentSnapshot, previousSnapshot)
    
    if file:
        file = (kovaaksPath + "/" + file)
        futils.clear_console()
        createAndApendDataFiles(file, dataPath, outPutPath, True, True)
        previousSnapshot = currentSnapshot
        
    time.sleep (2)

input = input()
