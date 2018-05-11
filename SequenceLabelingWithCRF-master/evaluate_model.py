import sys
import csv
import glob
import os

def getLabelData(testDir):
    fileMap = {}
    dialog_filenames = sorted(glob.glob(os.path.join(testDir, "*.csv")))
    for dialog_filename in dialog_filenames:
        with open(dialog_filename,"r") as f:
            labels = []
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            for row in data[1:]:
                labels.append(row[0])
            path = dialog_filename.split("\\")
            fileMap[path[-1]] = labels

    return fileMap

def getOutputLabels(outputFile):
    fileHandler = open(outputFile, "r")
    lines = fileHandler.readlines()
    fileMap = {}
    labels = []
    for line in lines:
        if "Filename=" in line:
            fileName = line.replace("Filename=\"","").replace("\"","").strip()
            labels = []
            fileMap[fileName] = labels
        elif line.strip() not in "":
            labels.append(line.strip())

    return fileMap


print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument
if len(sys.argv) != 3:
    print ('Please send file name as command line argument')
    exit(0)

devDir = sys.argv[1]
outputFile = sys.argv[2]

# get actual file names and labels
print ('devDir : ', devDir,' outputFile : ', outputFile)
fileMap = getLabelData(devDir)

# get file nmaes and labels from output.txt
outputFileMap = getOutputLabels(outputFile)

# count incorrect and total labels
incorrect = 0
total = 0
for key in fileMap.keys():
    acutalLabels = fileMap[key]
    predictedLabels = outputFileMap[key]
    wrong = 0
    total += len(acutalLabels)
    for label1, label2 in zip(acutalLabels, predictedLabels):
        if label1 != label2:
            wrong += 1
    incorrect += wrong
    print(key+" has "+str(wrong)+" incorrect labels and "+str((len(acutalLabels)-len(predictedLabels)))+" missing labels")

print("total label = "+str(total))
print("total incorrect = "+str(incorrect))

accuracy = ((total - incorrect)/total)*100
print("Accuracy = "+str(accuracy))

