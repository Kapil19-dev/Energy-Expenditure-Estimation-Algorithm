# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd
import math 
import copy 

#Representas an alpha user in our system
class AlphaUser():
    def __init__( self,
                   uid,
                   email,
                   username,
                   sex, 
                   age,
                   heightInches,
                   weightPounds):
        self.uid = uid
        self.email = email
        self.username = username
        self.sex = sex
        self.age = age
        self.heightInches = heightInches
        self.weightPounds = weightPounds 
        self.isAlpha = True

    def isMale(self):
        return self.sex == "M"

    def displayGender(self):
        if self.sex == None:
            return ""
        else:
            return self.sex
        
    def displayWeight(self):
        if self.weightPounds == None:
            return ""
        else:
            return str(self.weightPounds)
        
    def displayAge(self):
        if self.age == None:
            return ""
        else:
            return str(self.age)
        
    def displayHeight(self):
        if self.heightInches == None:
            return ""
        else:
            return str(inchesToFeetAndInches((self.heightInches)))
        
    def __str__(self):
        return ( "User id:  " +
                    str(self.uid).strip() +
                 "\nEmail:    " +
                     str(self.email) +
                 "\nUsername: " +
                     str(self.username) + 
                 "\nSex:      " +
                     self.displayGender() +
                 "\nAge:      " +
                     self.displayAge() +
                 "\nHeight:   " + 
                     self.displayHeight() +
                 "\nWeight:   " +
                     self.displayWeight() +
                 "\n-------------------------------------")
    

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
        self.age = round( age , 0 )
        self.heightInches = heightInches
        self.weightPounds = weightPounds
        self.bmi = bmi
        self.tdee = tdee
        self.activityLevel = activityLevel
        self.subjNum = subjNum
        self.isAlpha = False
        
    def isMale(self):
        return self.sex == "M"
    
    def getWeightKg(self):
        return lbsToKg(self.weightPounds)
    
    def getHeightCm(self):
        return inchesToCm(self.heightInches)
    
    def getHeightMeters(self):
        return inchesToMeters( self.heightInches )
    
    def getActivityMultiplier(self):
        return getActivityLevelNumVal(self.activityLevel)
        
    
    def __str__(self):
        return ( "Subject Number: " + str(self.subjNum ) + "\tSex: "+
                str(self.sex) + "\tAge: " + str(self.age) + "\tWeight: "+
                str(self.weightPounds)+ "\tHeight: " +
                str(inchesToFeetAndInches((self.heightInches))) + "\tBMI: "+
                str(self.bmi) + "\tTDEE: " + str(self.tdee) + 
                "\tActivity Level: " + str(self.activityLevel) + "\n" )
    

###########################   CONVERSIONS     ###############################
        
def getActivityLevelNumVal(activityLevel):
    if activityLevel == 'S':
        return 1.2
    elif activityLevel == "LA":
        return 1.375
    elif activityLevel == "A":
        return 1.55
    else:
        return 1.725

# converts a weight in kg to weight in lbs 
def kgToLbs( weightInKg ):
    return round( weightInKg * 2.2 , 2 )

#converts a weight in lbs to a weight in kg
def lbsToKg( weightInLbs ):
    return round( weightInLbs / 2 , 2 )

#converts a height in meters to a height in lbs
def metersToInches( heightInMeters ):
    return round( heightInMeters * 39.3701 , 2 )

#converts a height in inches to  a height in meters 
def inchesToMeters( heightInInches ):
    return round( heightInInches * 0.0254 , 2 )

#converts a height in inches to cm
def inchesToCm( heightInInches ):
    return round( heightInInches * 2.54 , 2 )

#converts a height in inches to as tring of the same height in ft and inches
def inchesToFeetAndInches( heightInInches ):
    feet =  math.floor( heightInInches / 12 ) 
    inches = math.floor( heightInInches % 12 )
    return str(feet)+"'"+str(inches)+"\""

#helper method for reutrning the correct gender string of alpha users 
def getGenderString(isMale):
    if isMale == True:
        return "M"
    elif isMale == False:
        return "F"
    else:
        return None 
    

##############################################################################

# helper method for clean data converts string to
# uppercase and trims it allows for only one call to map 
def upperTrim( string ):
    return string.upper().strip()

# measurements of energy expdentiture in dataset are separated 
# by commas and stored as strings, this function converts them 
# to an int 
def parseEnergyExpenditure( energyExpenditure):
    return int( energyExpenditure.replace(",","") )

# acts as a filter for joke heights entered by alpha users
#true if ridiculous
def ridiculousHeight( heightInches ):
    # unlikely anyone taller than 7 feet
    return heightInches > 84

# acts as a filter for joke weights entered by alpha users
#true if ridiculous
def ridiculousWeight( weightPounds ):
    #unlikely anyone bigger than 500 lbs
    return weightPounds  > 500

# opens raw data.csv and 'cleans' the data so it 
# can be used for analysis to create energy expenditure 
# estimation model. Returns a list of Subjects containing one 
# Subject for each row of the dataset.
def cleanSubjectData():
    rawData = getRawDataAsPandas()
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
                rowData[5], 
                upperTrim( rowData[6] ) ) 
        subjects.append( currentSubject )
    return subjects

#Opens up raw data file and returns as pandas array
def getRawDataAsPandas():
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
    #TDEE is stored as a string, change to 
    #int representations of EE's then replace 
    rawData['TDEE'] = list(map(parseEnergyExpenditure , rawData['TDEE']))
    return rawData

def genderAsNumeric(gender):
    if upperTrim(gender) == "M":
        return 1
    return 0
    

# opens raw alpha.csv and 'cleans' the data so it 
# can be used for analysis. Returns a list of alpha users
def cleanAlphaData():
    rawData = pd.read_csv("data/LS_Alpha_User_Data.csv")
    # build list of python class objects ( much easier to work with ) 
    alphaUsers = []
    for index, row in enumerate( rawData.iterrows() ):
        rowData= row[1].values
        
        uid = index
        email = rowData[1]
        username = rowData[4]
        sex = getGenderString(rowData[3])
        age = rowData[0]
        try:
            age = int(age)
        except:
            age = None
        height = rowData[2]
        try:
            height = int(height)
        except:
            height = None
        weight = rowData[5]
        try:
            weight = int(weight)
        except:
            weight = None
     
        alphaUsers.append( AlphaUser(uid,
                                     email,
                                     username,
                                     sex,
                                     age,
                                     height,
                                     weight))
    return alphaUsers

#calculates basic statistics about our sample. Like min max and avg for 
# different features. Also gives break down by gender. Does this in O(n) time.
def calculateStats(sample):
    # gender breakdown 
    numMale = 0
    numFemale = 0
    reportedGenders = 0
    
    # age
    minAge = 0
    maxAge = 0
    totalSampleAge = 0
    reportedAges = 0
    # height
    minHeight = 0
    maxHeight = 0
    totalSampleHeight = 0
    reportedHeights = 0
    
    # weight
    minWeight = 0
    maxWeight = 0
    totalSampleWeight = 0
    reportedWeights = 0
    
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
    
    for person in sample :
        
        if not person.sex == None:
            if person.sex == 'M':
                numMale+=1
            else:
                numFemale+=1
            reportedGenders+=1
            
        # Age
        if not person.age == None:
            if person.age < minAge or minAge == 0:
                minAge = person.age
            if person.age > maxAge:
                maxAge = person.age
            totalSampleAge += person.age
            reportedAges+=1
        
        # Height
        if not person.heightInches == None:
            if person.heightInches < minHeight or minHeight == 0:
                minHeight = person.heightInches
            if (person.heightInches > maxHeight and 
                not ridiculousHeight(person.heightInches)):
                maxHeight = person.heightInches
            totalSampleHeight += person.heightInches
            reportedHeights+=1
        
        # Weight
        if not person.weightPounds == None:
            if person.weightPounds < minWeight or minWeight == 0:
                minWeight = person.weightPounds
            if( person.weightPounds > maxWeight and
               not ridiculousWeight(person.weightPounds)):
                maxWeight = person.weightPounds
            totalSampleWeight += person.weightPounds
            reportedWeights+=1
        
        # Only 'subjects' have these properties
        if not person.isAlpha:
            # BMI
            if person.bmi < minTDEE or minBMI == 0:
                minBMI = person.bmi
            if person.bmi > maxBMI:
                maxBMI = person.bmi
            totalSampleBMI += person.bmi
        
            # TDEE
            if person.tdee < minTDEE or minTDEE == 0:
                minTDEE = person.tdee
            if person.tdee > maxTDEE:
                maxTDEE = person.tdee
            totalSampleTDEE += person.tdee
        
            #Activity level
            if person.activityLevel == 'S':
                numSedentary+=1
            elif person.activityLevel == "LA":
                numLightlyActive+=1
            elif person.activityLevel == "A":
                numActive+=1
            else:
                numVeryActive+=1;
            
    # output
    sampleSize = len(sample)
    print("<---GENDER---> ")
    print( "\tSample size:                   " + str( sampleSize))
    print( "\tNumber male:                   " + str(numMale))
    print( "\t\tPercentage male:       " +
          str(round((numMale/reportedGenders)*100,2))+"%")
    print( "\tNumber female:                 " + str(numFemale ))
    print( "\t\tPercentage female:     " +
          str(round((numFemale/reportedGenders)*100,2))+"%")
    
    print("<---AGE---> ")
    print( "\tMin age:                       " +  str(minAge) +" years")
    print( "\tAvg age:                       " +  
          str(round(totalSampleAge/reportedAges,2)) +" years")
    print( "\tMax age:                       " +  str(maxAge) + " years")
    
    print("<---HEIGHT---> ")
    print( "\tMin height:                    " +
          inchesToFeetAndInches( minHeight))
    print( "\tAvg height:                    " +
          inchesToFeetAndInches(( totalSampleHeight / reportedHeights  )))
    print( "\tMax height                     " +
          inchesToFeetAndInches( maxHeight))
    
    print("<---WEIGHT---> ")
    print( "\tMin weight:                    " +  str(round(minWeight,2)) +
          " lbs")
    print( "\tAvg weight:                    " +  
          str(round(totalSampleWeight/reportedWeights,2)) +" lbs")
    print( "\tMax weight:                    " +  str(round(maxWeight,2)) +
          " lbs")
    
    if not (sample[0]).isAlpha: # these stats only calculated for subjects
        print("<---BMI---> ")
        print( "\tMin BMI:                       " +  str(round(minBMI,2)) )
        print( "\tAvg BMI:                       " +  
              str(round(totalSampleBMI/sampleSize,2)) )
        print( "\tMax BMI:                       " +  str(round(maxBMI,2)) )
    
        print("<---TDEE---> ")
        print( "\tMin TDEE:                      " +  str(round( minTDEE,2)) )
        print( "\tAvg TDEE:                      " +  
              str(round(totalSampleTDEE/sampleSize,2)) )
        print( "\tMax TDEE:                      " +  str(round(maxTDEE,2)) )
    
        print("<---Activity Level---> ")
        print( "\tTotal number sedentary:        " +  str( numSedentary ) )
        print( "\t    Percentage sedentary:      " +  str(
                round( (numSedentary / sampleSize )*100 , 2 ) ) +"%" )
        print( "\tTotal number lightly active:   " +  str( numLightlyActive )) 
        print( "\t    Percentage lightly active: " +  str(
                round( (numLightlyActive / sampleSize )*100 , 2 ) ) +"%" )
        print( "\tTotal number active:           " +  str( numActive))
        print( "\t    Percentage active:         " +  str(
                round( (numActive / sampleSize )*100 , 2 ) ) +"%" )
        print( "\tTotal number very active:      " +  str( numVeryActive))
        print( "\t    Percentage very active:    " +  str(
                round( (numVeryActive / sampleSize )*100 , 2 ) ) +"%" )

        
    
#############################   MAIN     ###################################     
def main():
    # get subjects
    subjects = cleanSubjectData()
    maleSubjects = list( filter(   lambda sub: sub.sex == "M" ,
                          copy.deepcopy( subjects )))
    femaleSubjects = list( filter( lambda sub: sub.sex == "F" ,
                          copy.deepcopy( subjects )))
    # get alpha users
    alphaUsers = cleanAlphaData()
    maleAlphaUsers = list( filter(   lambda sub: sub.sex == "M" ,
                          copy.deepcopy( alphaUsers )))
    femaleAlphaUsers = list( filter( lambda sub: sub.sex == "F" ,
                          copy.deepcopy( alphaUsers )))
        
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Clean-Data)>").lower().strip()
        if userInput == '/help':
            print("\n" +
                  " /subjectData     =>\tPrint subject dataset\n" + 
                  " /subjectStats    =>\tAll subjects stats \n" +
                  " /maleSubjects    =>\tMale subjects stats\n" +
                  " /alphaData       =>\tPrint alpha dataset\n" + 
                  " /alphaStats      =>\tAll alpha stats \n" +
                  " /maleAlpha       =>\tMale alpha stats\n" +
                  " /femaleAlpha     =>\tFemale alpha stats\n" +
                  " /quit            =>\tEnd script" ) 
        #subject
        elif userInput == "/subjectdata" :
            for subject in subjects:
                print( subject )
        elif userInput == "/subjectstats":
            print("Stats for all subjects: ")
            calculateStats(subjects)
        elif userInput == "/malesubjects":
            print("Stats for male subjects only: ")
            calculateStats(maleSubjects)
        elif userInput == "/femalesubjects":
            print("Stats for female subjects only: ")
            calculateStats(femaleSubjects)
        #alpha
        elif userInput == "/alphadata" :
            for alphaUser in alphaUsers:
                print( alphaUser )
        elif userInput == "/alphastats":
            print("Stats for all alpha users: ")
            calculateStats(alphaUsers)
        elif userInput == "/malealpha":
            print("Stats for male alpha users only: ")
            calculateStats(maleAlphaUsers)
        elif userInput == "/femalealpha":
            print("Stats for female apha users only: ")
            calculateStats(femaleAlphaUsers)
        # utility   
        elif userInput == "/quit":
            print("\tTerminating Script  ")
            break
        else:
            print("\tFor list of commands:   '/help'")
            print("\t\tInvalid Input:  " + userInput)
    
##Tell python to run main function 
if __name__ == "__main__":
    main()