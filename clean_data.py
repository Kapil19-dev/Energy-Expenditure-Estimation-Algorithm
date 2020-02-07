# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd
import math 
import copy 

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
        
    def isMale():
        return self.sex == "M"
    
    def getActivityMultiplier():
        if self.activityLevel == 'S':
            return 1.2
        elif self.activityLevel == "LA":
            return 1.375
        elif self.activityLevel == "A":
            return 1.55
        else:
            return 1.725
        
    
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

#converts a weight in lbs to a weight in kg
def lbsToKg( weightInLbs ):
    return round( weightInLbs / 2 , 2 )

#converts a height in meters to a height in lbs
def metersToInches( heightInMeters ):
    return round( heightInMeters * 39.3701 , 2 )

#converts a height in inches to as tring of the same height in ft and inches
def inchesToFeetAndInches( heightInInches ):
    feet =  math.floor( heightInInches / 12 ) 
    inches = math.floor( heightInInches % 12 )
    return str(feet)+"'"+str(inches)+"\""

# measurements of energy expdentiture in dataset are separated 
# by commas and stored as strings, this function converts them 
# to an int 
def parseEnergyExpenditure( energyExpenditure):
    return int( energyExpenditure.replace(",","") )

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
                upperTrim( rowData[0] ), 
                rowData[1],
                metersToInches( rowData[2] ),
                kgToLbs( rowData[3] ),
                rowData[4],
                parseEnergyExpenditure(rowData[5]), 
                upperTrim( rowData[6] ) ) 
        subjects.append( currentSubject )
    return subjects

#calculates basic statistics about our sample. Like min max and avg for 
# different features. Also gives break down by gender. Does this in O(n) time.
def calculateStats(subjects):
    # gender breakdown 
    numMale = 0
    numFemale = 0
    # age
    minAge = 0
    maxAge = 0
    totalSampleAge = 0
    # height
    minHeight = 0
    maxHeight = 0
    totalSampleHeight = 0
    # weight
    minWeight = 0
    maxWeight = 0
    totalSampleWeight = 0
    # BMI 
    minBMI = 0
    maxBMI = 0
    totalSampleBMI = 0
    # TDEE 
    minTDEE = 0
    maxTDEE = 0
    totalSampleTDEE = 0
    # activity level breakdwon 
    numSedentary = 0
    numLightlyActive = 0
    numActive = 0
    numVeryActive = 0
    
    for subject in subjects :
        if subject.sex == 'M':
            numMale+=1
        else:
            numFemale+=1
            
        # Age
        if subject.age < minAge or minAge == 0:
            minAge = subject.age
        if subject.age > maxAge:
            maxAge = subject.age
        totalSampleAge += subject.age
        
        # Height
        if subject.heightInches < minHeight or minHeight == 0:
            minHeight = subject.heightInches
        if subject.heightInches > maxHeight:
            maxHeight = subject.heightInches
        totalSampleHeight += subject.heightInches
        
        # Weight
        if subject.weightPounds < minWeight or minWeight == 0:
            minWeight = subject.weightPounds
        if subject.weightPounds > maxWeight:
            maxWeight = subject.weightPounds
        totalSampleWeight += subject.weightPounds
        
        # BMI
        if subject.bmi < minTDEE or minBMI == 0:
            minBMI = subject.bmi
        if subject.bmi > maxBMI:
            maxBMI = subject.bmi
        totalSampleBMI += subject.bmi
        
        # TDEE
        if subject.tdee < minTDEE or minTDEE == 0:
            minTDEE = subject.tdee
        if subject.tdee > maxTDEE:
            maxTDEE = subject.tdee
        totalSampleTDEE += subject.tdee
        
        #Activity level
        if subject.activityLevel == 'S':
            numSedentary+=1
        elif subject.activityLevel == "LA":
            numLightlyActive+=1
        elif subject.activityLevel == "A":
            numActive+=1
        else:
            numVeryActive+=1;
            
    # output
    numSubjects = len(subjects)
    print("<---GENDER---> ")
    print( "\tTotal number subjects:         " + str( numSubjects))
    print( "\tNumber male subject:           " + str(numMale))
    print( "\t\tPercentage male:       " +
          str(round((numMale/numSubjects)*100,2))+"%")
    print( "\tNumber female subject:         " + str(numFemale ))
    print( "\t\tPercentage female:     " +
          str(round((numFemale/numSubjects)*100,2))+"%")
    
    print("<---AGE---> ")
    print( "\tMin age:                       " +  str(minAge) +" years")
    print( "\tAvg age:                       " +  
          str(round(totalSampleAge/numSubjects,2)) +" years")
    print( "\tMax age:                       " +  str(maxAge) + " years")
    
    print("<---HEIGHT---> ")
    print( "\tMin height:                    " +
          inchesToFeetAndInches( minHeight))
    print( "\tAvg height:                    " +
          inchesToFeetAndInches(( totalSampleHeight / numSubjects  )))
    print( "\tMax height                     " +
          inchesToFeetAndInches( maxHeight))
    
    print("<---WEIGHT---> ")
    print( "\tMin weight:                    " +  str(round(minWeight,2)) +
          " lbs")
    print( "\tAvg weight:                    " +  
          str(round(totalSampleWeight/numSubjects,2)) +" lbs")
    print( "\tMax weight:                    " +  str(round(maxWeight,2)) +
          " lbs")
    
    print("<---BMI---> ")
    print( "\tMin BMI:                       " +  str(round(minBMI,2)) )
    print( "\tAvg BMI:                       " +  
          str(round(totalSampleBMI/numSubjects,2)) )
    print( "\tMax BMI:                       " +  str(round(maxBMI,2)) )
    
    print("<---TDEE---> ")
    print( "\tMin TDEE:                      " +  str(round( minTDEE,2)) )
    print( "\tAvg TDEE:                      " +  
          str(round(totalSampleTDEE/numSubjects,2)) )
    print( "\tMax TDEE:                      " +  str(round(maxTDEE,2)) )
    
    print("<---Activity Level---> ")
    print( "\tTotal number sedentary:        " +  str( numSedentary ) )
    print( "\t    Percentage sedentary:      " +  str(
            round( (numSedentary / numSubjects)*100 , 2 ) ) +"%" )
    print( "\tTotal number lightly active:   " +  str( numLightlyActive )) 
    print( "\t    Percentage lightly active: " +  str(
            round( (numLightlyActive / numSubjects)*100 , 2 ) ) +"%" )
    print( "\tTotal number active:           " +  str( numActive))
    print( "\t    Percentage active:         " +  str(
            round( (numActive / numSubjects)*100 , 2 ) ) +"%" )
    print( "\tTotal number very active:      " +  str( numVeryActive))
    print( "\t    Percentage very active:    " +  str(
            round( (numVeryActive / numSubjects)*100 , 2 ) ) +"%" )

        
    
#############################   MAIN     ###################################     
def main():
    subjects = cleanData()
    male = list( filter(   lambda sub: sub.sex == "M" ,
                          copy.deepcopy( subjects )))
    female = list( filter( lambda sub: sub.sex == "F" ,
                          copy.deepcopy( subjects )))
        
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Clean-Data)>").lower().strip()
        if userInput == '/help':
            print(" /data   =>\tPrint dataset row by row \n" + 
                  " /stats  =>\tBreakdown of all subjects \n" +
                  " /male   =>\tBreakdown of male subjects \n" +
                  " /female =>\tBreakdown of female subjects \n" +
                  " /quit   =>\tEnd script" ) 
            
        elif userInput == "/data" :
            for subject in subjects:
                print( subject )
        elif userInput == "/stats":
            print("Stats for all subjects: ")
            calculateStats(subjects)
        elif userInput == "/male":
            print("Stats for male subjects only: ")
            calculateStats(male)
        elif userInput == "/female":
            print("Stats for female subjects only: ")
            calculateStats(female)
        elif userInput == "/quit":
            print("\tTerminating Script  ")
            break
        else:
            print("\tFor list of commands:   '/help'")
            print("\t\tInvalid Input:  " + userInput)
    
##Tell python to run main function 
if __name__ == "__main__":
    main()