import argparse
import collections
import csv
import numpy

'''
Open the Census File that contains 5 rows: row 1 is not used; row 2 is the state where the person lives, as
identified by a state ID number; row 3 is the person's annual income; row 4 is the industry in which the person
works; and row 5 is the occupation help by the person, as identified by an occupation code.
'''
parser = argparse.ArgumentParser(description = "Bang for your Buck Location Calculator")
parser.add_argument("census_data", type = str, help = "Csv file containing relevant housing data")
#parser.add_argument("census_data_directory", type = str, help = "Directory containing relevant census data")
parser.add_argument("-o", "--output_filename", type = str, default="BBLCoutput.csv", help = "Name of output file")
args = parser.parse_args()

with open(args.census_data) as f:
    reader = csv.reader(f, delimiter=",")
    census_array = list(reader)


'''
Build the data structure, which will be formatted as follows: there will be a dictionary whose keys are the 
occupations found in the css file, and whos associated values are a another dictionary to be created below, namely
subdictionary1.

subdictionary1 will have keys equal to each of the 50 states. Its associated values will be a list. The first entry
of this list will another list of every instance of annual income found in the csv file found in the associated state for the
associated occupation, namely the associated key in subdictionary1.  The second entry in the list will contain the median income
of the previous list.
'''
occupations = collections.OrderedDict()

#loop over each of the rows in the census csv file
for i in range(1, len(census_array)):
    jobCode = census_array[i][3]
    stateCode = census_array[i][1]
    wage = int(census_array[i][2])

    #if the occupation we're currently looking at does not already exist the dictionary
    if not jobCode in occupations:
        #create an entry in the dictionary for the occupation
        occupations[jobCode] = collections.OrderedDict()
    #if an instance of this occupation does not already exist in the state we are looking at
    if not stateCode in occupations[jobCode]:
        #create an entry for the state whose value is a list[a,b] s.t. a is a list with 
        #single entry = annual income on current line on csv file, b = placeholder for median (calculated later)
        occupations[jobCode][stateCode] = [[wage], 0]
    else:
        #we found a duplicate instance of occupation, so add the wage on this line to the list that holds the wages
        #for this job in this state
        occupations[jobCode][stateCode][0].append(wage)

#loop to compute the medians
for i in occupations:
    for j in occupations[i]:
        occupations[i][j][1] += numpy.median(occupations[i][j][0])

print occupations['5380']['1'][1]
