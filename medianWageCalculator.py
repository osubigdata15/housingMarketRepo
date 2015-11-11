import sys
import argparse
import collections
import csv
import numpy

parser = argparse.ArgumentParser(description = "Bang for your Buck Location Calculator")
parser.add_argument("census_data", type = str, help = "Csv file containing relevant census data")
#parser.add_argument("census_data_directory", type = str, help = "Directory containing relevant census data")
parser.add_argument("-o", "--output_filename", type = str, default="BBLCoutput.csv", help = "Name of output file")
args = parser.parse_args()


'''
Opens the Census File that contains 5 rows: row 1 is not used; row 2 is the state where the person lives, as
identified by a state ID number; row 3 is the person's annual income; row 4 is the industry in which the person
works; and row 5 is the occupation help by the person, as identified by an occupation code.
'''
with open(args.census_data) as f:
    reader = csv.reader(f, delimiter=",")
    census_array = list(reader)


'''
Builds the data structure, which will be formatted as follows: there will be a dictionary whose keys are the 
occupations found in the css file, and whos associated values are a another dictionary to be created below, namely
subdictionary1.

subdictionary1 will have keys equal to each of the 50 states. Its associated values will be a list. The first entry
of this list will another list of every instance of annual income found in the csv file found in the associated state for the
associated occupation, namely the associated key in subdictionary1.  The second entry in the list will contain the median income
of the previous list.
'''
def createDict(census_array):
    result = collections.OrderedDict()

    #loop over each of the rows in the census csv file
    for i in range(1, len(census_array)):
        jobCode = census_array[i][4]
        stateCode = census_array[i][1]
        wage = int(census_array[i][2])

        #if the occupation we're currently looking at does not already exist the dictionary
        if not jobCode in result:
            #create an entry in the dictionary for the occupation
            result[jobCode] = collections.OrderedDict()
        #if an instance of this occupation does not already exist in the state we are looking at
        if not stateCode in result[jobCode]:
            #create an entry for the state whose value is a list[a,b] s.t. a is a list with a
            #single entry equal to the annual income on the current line on csv file, and b equal 
            # to a placeholder for the median (calculated later)
            result[jobCode][stateCode] = [[wage], 0]
        else:
            #we found a duplicate instance of occupation, so add the wage on this line to the list that holds the wages
            #for this job in this state
            result[jobCode][stateCode][0].append(wage)

    #loop to compute the medians
    for i in result:
        for j in result[i]:
            result[i][j][1] += numpy.median(result[i][j][0])

    return result

#the dictionary holding all the median salary data
occupations = createDict(census_array)


'''
Outputs the generated data structure as a new csv file. Each unique occupation ID will constitute, 
a table row, whose columns will be linked each of the 50 states plus Washington D.C. The cells of the
table body will then be filled with the corresponding median incomes of wage earners in each industry 
per state.
'''
with open("/Users/G7Kellen/Documents/JuniorYear/BDAA/OUTPUT/salaries_per_ind_per_st.csv", "w") as fOut:
    writer = csv.writer(fOut, delimiter = ",")

    #a list of every state code, corresponding to the states in alabetical order
    stateList = [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,
    24,25,26,27,28,29,30,31,32,33,34]

    #the rest of the states whose data I couldn't download
    #,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]
    #create the first row (header) of the output file

    #used distinguish states with no jobs given industry, as decided upon by our team 
    NO_JOBS = "--"

    #begin by creating a list that will be repeatedly updated with the eventual rows of the csv file.
    row = [""]
    for i in range(0, len(stateList)):
        row.append(`stateList[i]`)

    writer.writerow(row)
    row = []


    #looping over every unique occupation in the dictionary structure we created
    for job in occupations:
        #append to the row the occupaton name
        row.append(job);

        #for every state associated with the current occupation
        for state in stateList:
            stateStr = str(state)
         
            #append to the row the median salary of this occupation found in the current state
            if stateStr in occupations[job]:
                if occupations[job][stateStr][1] > 0:
                    row.append(occupations[job][stateStr][1])    
                else:
                    row.append(NO_JOBS)
            else:
                row.append(NO_JOBS)

        #write the row to the csv file, then reset it in time for the next row
        writer.writerow(row)
        row = []





