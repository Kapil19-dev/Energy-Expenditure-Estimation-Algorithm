# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""

import clean_data as cleaner 
import classes as classes
import csv 

# Returns a list of objects that contain different estimates of TDEE 
# for a given subject. 
def buildEnergyExpenditureResults():
    subjectList = cleaner.getSubjects()
    results = []
    for subject in subjectList:
        results.append( classes.SubjectEnergyResults(subject) )
    return results   

# Calculates min max and average difference for estimation techniques from
# true measure of TDEE for a subject 
def testAndCompareModels( resultList):
    managers = [ classes.EnergyComparisonResult("originalHarrisBenedict"),
                 classes.EnergyComparisonResult("revisedHarrisBenedict"),
                 classes.EnergyComparisonResult("mifflinStJeor"),
                 classes.EnergyComparisonResult("owen"),
                 classes.EnergyComparisonResult("whoFaoUnu"),
                 classes.EnergyComparisonResult("logSmarter") ]
    
    for result in resultList:
        for manager in managers:
            manager.updateForSubjectResult(result)
                
    return managers

#########################  GLOBAL VARIABLES ##########################         
subjectResultsList = buildEnergyExpenditureResults()
managers = testAndCompareModels( subjectResultsList )
######################################################################


#Exports errors from different extimation techniques to CSV
def exportResultsAndErrors( energyResultsList ):
    
    #### SORT BY ONES WHERE HARRIS BENEDICT BEATS LS BY MOST
    sortedResultsList = sorted( energyResultsList, key=lambda result:
         abs(result.trueTDEE - result.logSmarter) - abs(
                 result.trueTDEE - result.revisedHarrisBenedict), reverse=True)
    with open('data/error.csv' , 'w', newline='' ) as writeFile:
        writer = csv.writer( writeFile )
        rowList = []
        colHeaders = [ "subjNum","TDEE",
                       "originalHarris","originalHarrisError",
                       "revisedHarris","revisedHarrisError",
                       "whoFaoUnu","whoFaoUnuError",
                       "owen","owenError",      
                       "mifflinStJeor","mifflinStJeorError",
                       "logSmarter","logSmarterError",
                       "optimal","optimalError",
                       "Sex","Age","HeightInches","WeightPounds",
                       "bmi", "activityLevel"]
    
        rowList.append( colHeaders )
        # Sort list with higher LS errors at top, want to find demographic  
        # that we are overestimating for 
        for result in sortedResultsList:
            errorRow = result.toErrorRow()
            # sort by rows where LSDiff > RevisedHarrisDiff
            harrisDiffLS = abs(result.trueTDEE - result.logSmarter) - abs(
                    result.trueTDEE - result.revisedHarrisBenedict)  
            errorRow.append(harrisDiffLS)
            rowList.append(errorRow)
  
        writer.writerows( rowList )
        writeFile.close()
    
#############################   MAIN     #####################################
def main():
    global subjectResultsList
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Test-Model)>").lower().strip()
        if userInput == '/help':
            print("\n" +
                  " /tdeeData        =>\tPrint tdee result dataset\n"+
                  " /bmrData         =>\tPrint bmr result dataset\n"+
                  " /compare         =>\tPrint TDEE estimation comparison\n"+
                  " /compareOpt      =>\tCompares with optimal\n"+
                  " /export          =>\tExports results and errors\n"+
                  " /quit            =>\tEnd script" ) 
        #results
        elif userInput == "/tdeedata" :
            for result in subjectResultsList:
                print( result )
        elif userInput == "/bmrdata" :
            for result in subjectResultsList:
                print( result.bmrToString() )
        elif userInput == "/compare" :
            for manager in managers:
                print( manager )
        elif userInput == "/export" :
            exportResultsAndErrors(subjectResultsList)
            print("\n\tExported results and result errors to data/error.csv\n")

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