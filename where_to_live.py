import argparse
import collections
import csv
import numpy

parser = argparse.ArgumentParser(description = "Bang for your Buck Location Calculator")
parser.add_argument("median_income_file", type = str, help = "Csv file containing median wage information")
parser.add_argument("zillow_data", type = str, help = "Csv file containing zhvi indexes for all states")
parser.add_argument("occupation", type = str, help = "Occupation code")

args = parser.parse_args()

state_code_path = "state_codes.csv"
occupation = args.occupation
def toFloat(x):
    try:
        return float(x)
    except ValueError:
        return 0


def createZillowDict(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        housing_array = list(reader)
    d = {}
    for i in range(1, len(housing_array)):
	d[housing_array[i][1]] = housing_array[i][3]
    return d

with open(state_code_path, 'Ur') as f:
    reader = csv.reader(f, delimiter=",")
    stateDict = dict(reader)

with open(args.median_income_file) as f:
    reader = csv.reader(f, delimiter=",")

    #column 0 is occupation code. all other columns are median wage per state.
    wageArray = list(reader)
    wageDict = {}
    for i in range(1, len(wageArray)):
        code = wageArray[i][0]
        wagesPerState = {}
        for j in range(1, len(wageArray[i])):
            
            state = wageArray[0][j]
            wagesPerState[state]=(wageArray[i][j])
        wageDict[code]=wagesPerState



zillowDict = createZillowDict(args.zillow_data)
BBDict = collections.OrderedDict()

zeroStates = ['20', '23','56']

#print toInt(wageDict[occupation]['54'])
#print toInt(zillowDict[stateDict['54']])

#want Dictionary of State: wage-homecost
for state in stateDict:
    
    if state not in zeroStates:
        BBDict[stateDict[state]]= toFloat(wageDict[occupation][state])- toFloat(zillowDict[stateDict[state]])

#print BBDict

#maine, kansas, and wyoming have no zillow data


BBDict = collections.OrderedDict(sorted(BBDict.iteritems(), key=lambda x: x[1], reverse = True))
i = 0
print "The top five places for you to live are: "
for entry in BBDict:
    if(i < 5):
        print entry
        i+=1
    else:
        break

fileOutName = "BFYB_"+str(occupation)+".csv"
with open(fileOutName, 'w') as f:
    output = []
    for entry in BBDict:
        output.append(entry)
    print >> f, ",".join(output)
    output = []
    for entry in BBDict:
        output.append(str(BBDict[entry]))
    print >> f, ",".join(output)



