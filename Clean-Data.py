# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd
import math 

#Python class object that represents  
class Subject():
    def __init__( self,
                   subjNum,
                   sex, 
                   age,
                   heightInches,
                   weightPounds,
                   bmi,
                   tdee,
                   activityLevel):
        self.sex = sex
        self.age = age
        self.heightInches = heightInches
        self.weightPounds = weightPounds
        self.bmi = bmi
        self.tdee = tdee
        self.activityLevel = activityLevel
        self.subjNum = subjNum
    
    def __str__(self):
        return ( "Subject Number: " + str(self.subjNum ) + "\tSex: "+
                str(self.sex) + "\tAge: " + str(self.age) + "\tWeight: "+
                str(self.weightPounds)+ "\tHeight: " +
                str(inchesToFeetAndInches((self.heightInches))) + "\tBMI: "+
                str(self.bmi) + "\tTDEE: " + str(self.tdee) + 
                "\tActivity Level: " + str(self.activityLevel) + "\n" )
    
    
# helper method for clean data converts string to
# uppercase and trims it allows for only one call to map 
def upperTrim( string ):
    return string.upper().strip()

# converts a weight in kg to weight in lbs 
def kgToLbs( weightInKg ):
    return round( weightInKg * 2.2 , 2 )

#converts a height in meters to a height in lbs
def metersToInches( heightInMeters ):
    return round( heightInMeters * 39.3701 , 2 )

#converts a height in inches to as tring of the same height in ft and inches
def inchesToFeetAndInches( heightInInches ):
    feet =  math.floor( heightInInches / 12 ) 
    inches = math.floor( heightInInches % 12 )
    return str(feet)+"'"+str(inches)+"\""

# opens raw data.csv and 'cleans' the data so it 
# can be used for analysis to create energy expenditure 
# estimation model. Returns a list of Subjects containing one 
# Subject for each row of the dataset.
def cleanData():
    rawData = pd.read_csv("data/DLW_TDEE_DATA.csv")
    # only 766 rows of data but read_csv returns 1467 rows
    # drop other 701 rows to only retain headers and
    # rows of interest
    rawData.drop( rawData.tail(701).index ,inplace=True )
    #drop columns that are not of interest 
    colsToDrop = [5,7,9,10,11,12,13,14,
                  15,16,17,18,19,20,21,
                  22,23,24,25]
    rawData.drop(rawData.columns[colsToDrop],axis=1,inplace=True)
    #consistent format for column names 
    rawData.columns = map( upperTrim , rawData.columns )
    #consistent with acronym for energy expenditure 
    rawData.rename( columns = {'TEE':'TDEE'} , inplace= True )
    # build list of python class objects ( much easier to work with ) 
    subjects = []
    for index, row in enumerate( rawData.iterrows() ):
        rowData = row[1].values
        currentSubject = Subject( 
                index,
                rowData[0], 
                rowData[1],
                metersToInches( rowData[2] ),
                kgToLbs( rowData[3] ),
                rowData[4],
                rowData[5], 
                rowData[6]) 
        subjects.append( currentSubject )
    return subjects

#calculates basic statistics about our sample. Like min max and avg for 
# different features. Also gives break down by gender.
def calculateStats(subjects):
    print( "NOT IMPLEMENTED YET" )

#############################   MAIN     ###################################     
def main():
    subjects = cleanData()
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Clean-Data)>").lower().strip()
        if userInput == '/help':
            print(" /data  => Print dataset row by row \n" + 
                  " /stats => Basic breakdown of dataset \n" +
                  " /quit  => End script" ) 
        elif userInput == "/data" :
            for subject in subjects:
                print( subject )
        elif userInput == "/stats":
            calculateStats(subjects)
        elif userInput == "/quit":
            print("\tTerminating Script  ")
            break
        else:
            print("\tFor list of commands:   '/help'")
            print("\t\tInvalid Input:  " + userInput)
    
##Tell python to run main function 
if __name__ == "__main__":
    main()