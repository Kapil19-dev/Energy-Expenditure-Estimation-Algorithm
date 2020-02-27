# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd
import copy 
import classes as classes
import helper as helpers

#Opens up raw data file and returns as pandas array
def cleanRawDataAsPandas():
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
    rawData.columns = map( helpers.upperTrim , rawData.columns )
    #consistent with acronym for energy expenditure 
    rawData.rename( columns = {'TEE':'TDEE'} , inplace= True )
    #TDEE is stored as a string, change to 
    #int representations of EE's then replace 
    rawData['TDEE'] = list(map(helpers.parseEnergyExpenditure , rawData['TDEE']))
    return rawData

# opens raw data.csv and 'cleans' the data so it 
# can be used for analysis to create energy expenditure 
# estimation model. Returns a list of Subjects containing one 
# Subject for each row of the dataset. Raw data param is a pandas 
# dataframe containing the cleaned DLW data set
def cleanSubjectData(rawData):
    # build list of python class objects ( much easier to work with ) 
    subjects = []
    for index, row in enumerate( rawData.iterrows() ):
        rowData = row[1].values
        currentSubject = classes.Subject( 
                index,
                helpers.upperTrim( rowData[0] ), 
                rowData[1],
                helpers.metersToInches( rowData[2] ),
                helpers.kgToLbs( rowData[3] ),
                rowData[4],
                rowData[5], 
                helpers.upperTrim( rowData[6] ) ) 
        subjects.append( currentSubject )
    return subjects

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
        sex = helpers.getGenderString(rowData[3])
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
     
        alphaUsers.append( classes.AlphaUser(uid,
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
    managers = [classes.CatagoricalStatManager("SEX","sex")  ,
                classes.NumericStatManager("Age","years","age"),
                classes.NumericStatManager("Height","in","heightInches"), 
                classes.NumericStatManager("Weight","lbs","weightPounds") ]  
    if not isAlpha:
        managers.extend((classes.CatagoricalStatManager("PALCAT","activityLevel"),
                        classes.NumericStatManager( "BMI" ,"kg/m(^2)","bmi" ) ,
                        classes.NumericStatManager( "TDEE","kcal","tdee" )))
    
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

############################ GLOBAL VARIABLES ###############################
pandasData = cleanRawDataAsPandas().copy()
subjects = cleanSubjectData( pandasData )
#############################################################################

#Helpers for accessing global variables
def getRawDataAsPandas():
    global pandasData
    return pandasData

def getSubjects():
    global subjects     
    return subjects 

############################      MAIN       ################################   
def main():
    global subjects
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
        userInput = input("(Clean-Data)> ").lower().strip()
        if userInput == '/help':
            print("\n" +
                  " /subjectData     =>\tPrint subject dataset\n" + 
                  " /subjectStats    =>\tAll subjects stats \n" +
                  " /maleSubjects    =>\tMale subjects stats\n" +
                  " /femaleSubjects  =>\tFemale subjects stats\n" +
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