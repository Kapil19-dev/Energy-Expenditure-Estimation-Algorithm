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
        
#Helper class for accumulating and calculating numeric subject stats
class NumericStatManager():
    def __init__(  self,
                   statName, 
                   statUnits,
                   subjPropertyName):
        self.name = statName
        self.min = 0
        self.max = 0
        self.total = 0
        self.reported = 0
        self.units = statUnits 
        self.values = []
        self.subjPropertyName = subjPropertyName
        #q1,q2,q3,IQR
        self.quartiles = ( 0,0,0,0 )
        
    # adds data for a stat to the manager    
    def update( self, subject ):
        value = getattr(subject,self.subjPropertyName)
        if value < self.min or self.min == 0:
            self.min = value
        if value > self.max or self.max == 0:
            self.max = value
        self.total += value
        self.reported += 1
        self.values.append( value )
        self.updateQuartiles()
        
    #returns a tuple 
    def updateQuartiles(self):
        self.values.sort()
        idxOfQ1 = round( self.reported * ( 1/4 ) )
        idxOfQ2 = round( self.reported * ( 2/4 ) )
        idxOfQ3 = round( self.reported * ( 3/4 ) )
        if ( ( idxOfQ1 > -1 and idxOfQ1 < self.reported ) and
             ( idxOfQ2 > -1 and idxOfQ2 < self.reported ) and
             ( idxOfQ3 > -1 and idxOfQ3 < self.reported ) ):
            iqr = round( self.values[idxOfQ3] - self.values[idxOfQ1] )
            self.quartiles = (self.values[idxOfQ1], #Q1
                              self.values[idxOfQ2], #Q2
                              self.values[idxOfQ3], #Q3
                              iqr)
            
    #returns which bucket a value falls into
    # val <= q1 is low
    # q1 < val < q3 is avg 
    # val >= q3 is high
    def getBucketForSubject(self,subj):
        val = getattr(subj,self.subjPropertyName)
        bucket = ""
        q1 = self.quartiles[0]
        q2 = self.quartiles[1]
        q3 = self.quartiles[3]
        if val <= q1:
            bucket = "low"
        elif q1 < val and val < q3:
            bucket = "avg"
        elif val >= q3:
            bucket =  "high"
        return bucket+"-"+self.name
                    
    def __str__(self):
        return("<---"+self.name+"---> " +
         "\n\tMin "+self.name+":                 " +
              str(round(self.min,2)) + " " + self.units +
         "\n\tAvg " +self.name+":                 " +
              str(round(self.total/self.reported,2)) + " " + self.units +
         "\n\tMax " +self.name+":                 " +
              str(round(self.max,2)) + " " + self.units +
          "\n\tQ1:                          " + str(self.quartiles[0])  +
          "\n\tQ2:                          " + str(self.quartiles[1])  +
          "\n\tQ3:                          " + str(self.quartiles[2])  +
          "\n\tIQR:                         " + str(self.quartiles[3]))
    #true if empty
    def isEmpty(self):
        return self.reported == 0 
    
#Helper class for accumulating and calculating catagorical subject stats
class CatagoricalStatManager():
    def __init__(  self,
                   statName,
                   subjPropertyName):
        self.name = statName
        # keeps track of occurences of each catagory in the dataset
        self.catagoryCounts = {}
        self.subjPropertyName = subjPropertyName
        self.reported = 0
        
        
     # helper for building bucket key for subjects   
    def getBucketForSubject(self,subject):
        bucket = getattr(subject,self.subjPropertyName)
        return bucket +"-"+ self.name
        
        
    #updates count of category that value is in and num of reports
    def update( self, subject ):
        value = getattr(subject,self.subjPropertyName)
        if not value in self.catagoryCounts.keys():
            self.catagoryCounts[value] = 0
        self.catagoryCounts[value] += 1
        self.reported += 1 
    
    def __str__(self):
        retStr = "<---"+self.name+"---> "
        if self.isEmpty():
            retStr += "\n NO STATS "
        else:
            for key , value in self.catagoryCounts.items():
                retStr += ( "\n\t Total " + key +  ": " + 
                           strRound( value, 2  ) + "\n\t\t % " + key +
                           ": " +strRound((value/self.reported)*100,2 )+"%")
        return retStr
    
    #true if empty
    def isEmpty(self):
        return self.reported == 0 
        
###########################   CONVERSIONS     ###############################
# converts activity level from string -> num
def getActivityLevelNumVal(activityLevel):
    activityLevel = upperTrim(activityLevel)
    if activityLevel == 'S':
        return 1.2
    elif activityLevel == "LA":
        return 1.375
    elif activityLevel == "A":
        return 1.55
    else:
        return 1.725

#converts gender from string -> num
def genderAsNumeric(gender):
    if upperTrim(gender) == "M":
        return 2
    return 1

#helper method for reutrning the correct gender string of alpha users 
def getGenderString(isMale):
    if isMale == True:
        return "M"
    elif isMale == False:
        return "F"
    else:
        return None 
    

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

#converts a number to a string, rounded to dec decimal places
#needed helper for this because I do it alot 
def strRound( number , dec ):
    return str( round( number , dec ) )

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
# also returns a list of the stat managers
def calculateStats(sample , shouldPrint ):
    isAlpha = (sample[0]).isAlpha
    managers = [CatagoricalStatManager("SEX","sex")  ,
                NumericStatManager("Age","years","age"),
                NumericStatManager("Height","in","heightInches"), 
                NumericStatManager("Weight","lbs","weightPounds") ]  
    if not isAlpha:
        managers.extend((CatagoricalStatManager("PALCAT","activityLevel"),
                        NumericStatManager( "BMI" ,"kg/m(^2)","bmi" ) ,
                        NumericStatManager( "TDEE","kcal","tdee" )))
    
    #calc stats
    for person in sample:
        for manager in managers:
            if not (getattr( person , manager.subjPropertyName ) == None):
                manager.update(person)
            
    # output
    if shouldPrint:
        for manager in managers:
            print( manager )
    
    # stat managers returned
    return managers

            
# returns a dictionary where keys are properties that describe a bucket and 
# the values are list of subjects who fall in that bucket 
def getBucketDictionary( subjects ):
    # first filter out tdee. Wouldn't make sense to have target considered 
    # in buckets
    managers = calculateStats( subjects , False )
    managers = list(filter(lambda man:  man.name != "TDEE" , managers) )
    
    ## mapping from bucketKey -> list of usbjects in bucket 
    bucketDict = {}
    
    for subject in subjects:
        bucketKey =""
        for manager in managers:
            bucketKey += manager.getBucketForSubject(subject)+"_"
        if not bucketKey in bucketDict.keys():
            bucketDict[bucketKey] = []
        bucketDict[bucketKey].append(subject)
        
    return bucketDict
        
    

        
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
                  " /buckets         =>\tPrints all buckets \n" +
                  " /quit            =>\tEnd script" ) 
        #subject
        elif userInput == "/subjectdata" :
            for subject in subjects:
                print( subject )
        elif userInput == "/subjectstats":
            print("Stats for all subjects: ")
            calculateStats(subjects,True)
        elif userInput == "/malesubjects":
            print("Stats for male subjects only: ")
            calculateStats(maleSubjects,True)
        elif userInput == "/femalesubjects":
            print("Stats for female subjects only: ")
            calculateStats(femaleSubjects,True)
        #alpha
        elif userInput == "/alphadata" :
            for alphaUser in alphaUsers:
                print( alphaUser )
        elif userInput == "/alphastats":
            print("Stats for all alpha users: ")
            calculateStats(alphaUsers,True)
        elif userInput == "/malealpha":
            print("Stats for male alpha users only: ")
            calculateStats(maleAlphaUsers,True)
        elif userInput == "/femalealpha":
            print("Stats for female apha users only: ")
            calculateStats(femaleAlphaUsers,True)
        elif userInput == "/buckets":
            print("All buckets in subject data: ")
            buckets = getBucketDictionary(subjects)
            for bucketKey in buckets.keys():
                print("\n"+bucketKey) 
                print("\tSubjects in bucket: "+ str(len(buckets[bucketKey])))
            print("\n Total buckets: " + str(len(buckets.keys())))
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