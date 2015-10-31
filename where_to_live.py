import argparse
import collections
import csv
import numpy

parser = argparse.ArgumentParser(description = "Bang for your Buck Location Calculator")
parser.add_argument("median_income_file", type = str, help = "Csv file containing median wage information")
parser.add_argument("zillow_data", type = str, help = "Csv file containing zhvi indexes for all states")
args = parser.parse_args()

state_code_path = "state_codes.csv"
occupation = "5380"
def toInt(x):
    try:
        return int(x)
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


with open(args.median_income_file) as f:
    reader = csv.reader(f, delimiter=",")

    #column 0 is occupation code. all other columns are median wage per state.
    wageArray = list(reader)
    wageDict = {}
    for i in range(1, len(wageArray)):
        state = wageArray[i][0]
        wages = []
        for j in range(1, len(wageArray[i])):
            wages.append(wageArray[i][j])
        wageDict[state]=wages

with open(state_code_path) as f:
    reader = csv.reader(f, delimiter=",")

    #column 0 is occupation code. all other columns are median wage per state.
    stateDict = dict(reader)

zillowDict = createZillowDict(args.zillow_data)
BBDict = {}

#want Dictionary of State: wage-homecost

i=0
for state in stateDict:
    BBDict[stateDict[state]]=toInt(wageDict[occupation][i])-toInt(zillowDict[stateDict[state]])
    i+=1

print BBDict

#maine, kansas, and wyoming have no zillow data


