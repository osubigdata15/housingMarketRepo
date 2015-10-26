import argparse
import csv


def createLongTermDict(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        housing_array = list(reader)
    dict = {}
    for i in range(1, len(housing_array)):
        temp = []
        for j in range(1, len(housing_array[i])):
            temp.append(housing_array[i][j])
            dict[housing_array[i][0]]=temp
    return dict

parser = argparse.ArgumentParser(description = "Bang for your Buck Location Calculator")
parser.add_argument("housing_data", type = str, help = "Csv file containing relevant housing data")
#parser.add_argument("census_data_directory", type = str, help = "Directory containing relevant census data")
parser.add_argument("-o", "--output_filename", type = str, default="BBLCoutput.csv", help = "Name of output file")
args = parser.parse_args()


newDict = createLongTermDict(args.housing_data)



print newDict['New Jersey']
