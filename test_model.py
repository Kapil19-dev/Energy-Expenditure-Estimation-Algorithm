# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""

import clean_data as cleaner 
import train_model as LogSmarter
import math
import csv 

class SubjectEnergyResults():
    #constructor
    def __init__( self,subject):
        self.subject = subject
        self.subjectID = subject.subjNum
        self.trueTDEE = subject.tdee
        self.logSmarter = getLogSmarter( subject )
        ############## BELOW ARE BMR ESTIMATES #########################
        # TDEE = BMR estimate * activityLevel
        # below is a comprehensive source of all popular estimation methods
        # https://completehumanperformance.com/2013/10/08/calorie-needs/
        self.originalHarrisBenedict = (getOriginalHarrisBenedict( subject ) *
                                       subject.getActivityMultiplier() )
        self.revisedHarrisBenedict = (getRevisedHarrisBenedict( subject ) *
                                      subject.getActivityMultiplier() )
        self.mifflinStJeor = (getMifflinStJeor(subject) *
                              subject.getActivityMultiplier() )
        self.whoFaoUnu = ( getWhoFaoUnu(subject) *
                          subject.getActivityMultiplier() )
        self.owen = getOwen(subject) * subject.getActivityMultiplier() 

    #converts to string
    def __str__(self):
        return ( "Subject Number: " + str(self.subjectID) + "\n"
                "\n\tTrue TDEE:                " +
                    str(round(self.trueTDEE,0) ) +
                "\n\tLogSmarter:               " +
                    removeTrailing(str(round(self.logSmarter,0))) +
                "\n---------- TDEE ESTIMATES -----------" +
                "\n\tOriginal Harris Benedict: " +
                    removeTrailing(str(round(self.originalHarrisBenedict,0)))+ 
                "\n\tRevised Harris Benedict:  " +
                    removeTrailing(str(round(self.revisedHarrisBenedict,0)))+
                "\n\tMifflin-St Jeor:          " +
                    removeTrailing(str(round(self.mifflinStJeor,0))) +
                "\n\tOwen:                     " +
                    removeTrailing(str(round(self.owen,0))) +
                "\n\tWHO-FAO-UNU:              " +
                    removeTrailing(str(round(self.whoFaoUnu,0))) +
                "\n--------------------------------------------------"
                )
    
    #converts to row for exporting error to csv, displays each TDEE estimate
    # along with absolute error for comparison 
    def toErrorRow(self):
        originalHarrisError =  abs(self.trueTDEE - self.originalHarrisBenedict)
        revisedHarrisError =  abs(self.trueTDEE - self.revisedHarrisBenedict)
        owenError = abs(self.trueTDEE - self.owen)
        mifflinStJeorError = abs(self.trueTDEE- self.mifflinStJeor )
        whoFaoUnuError = abs( self.trueTDEE - self.whoFaoUnu )
        logSmarterError = abs(self.trueTDEE- self.logSmarter) 
        return [ self.subjectID, self.trueTDEE, 
                 round(self.originalHarrisBenedict,2),
                 round(originalHarrisError,2),
                 round(self.revisedHarrisBenedict,2), 
                 round(revisedHarrisError,2),
                 round(self.whoFaoUnu,2),
                 round(whoFaoUnuError,2),
                 round(self.owen,2), 
                 round(owenError,2),
                 round(self.mifflinStJeor,2),
                 round(mifflinStJeorError,2),
                 round(self.logSmarter,2), 
                 round(logSmarterError,2),
                 self.subject.sex , self.subject.age,
                 self.subject.heightInches, self.subject.weightPounds,
                 self.subject.bmi, self.subject.activityLevel]
        
    # Prints estimates of BMR instead of TDEE
    def bmrToString(self):
        return ( "Subject Number: " + str(self.subjectID) + "\n"
                "\n\tTrue TDEE:                " +
                    str(round(self.trueTDEE,0) ) +
                "\n\tLogSmarter:               " +
                    removeTrailing(str(round(self.logSmarter,0))) +
                "\n---------- BMR ESTIMATES -----------" + 
                "\n\tOriginal Harris Benedict: " +
                    removeTrailing(str(round(self.originalHarrisBenedict / 
                                self.subject.getActivityMultiplier() ,0)))+ 
                "\n\tRevised Harris Benedict:  " +
                    removeTrailing(str(round(self.revisedHarrisBenedict /
                                self.subject.getActivityMultiplier() ,0)))+
                "\n\tMifflin-St Jeor:          " +
                    removeTrailing(str(round(self.mifflinStJeor /
                                self.subject.getActivityMultiplier(),0))) +
                "\n\tOwen:                     " +
                    removeTrailing(str(round(self.owen / 
                                self.subject.getActivityMultiplier(),0))) +
                "\n\tWHO-FAO-UNU:              " +
                    removeTrailing(str(round(self.whoFaoUnu /
                                self.subject.getActivityMultiplier(),0))) +
                "\n--------------------------------------------------")


# Helper class for calculating the min max and avgs of EE's
# greatly reduces need for repeat code 
class EnergyComparisonResult():
    
    def __init__( self , name ):
            self.techniqueName = name 
            self.min = 0
            self.max = 0
            self.total = 0
            self.absTotal = 0
            #Accumulator for MSE
            #RMSE seems like best estimate her
            self.sumObservedPredictedDiffSquared = 0
            # total number of subjects we've added data for
            self.count = 0
    
    #updates min max and avg for a subjects difference from their 
    # true estimate for a given technique 
    def updateForNewSubject( self, estimate , actual  ):
        difference = actual - estimate 
        if ( difference < self.min or self.min == 0 ):
            self.min = difference
        if( difference > self.max or self.max == 0):
            self.max = difference
        self.total += difference
        #Mean absolute error
        self.absTotal += abs(difference)
        self.sumObservedPredictedDiffSquared = ( ( actual - estimate ) ** 2 )
        self.count+=1
    
    def __str__(self):
        return("<--- " + self.techniqueName + " ---> " +
         "\n\tMin difference:                   " + 
             str(round(self.min,2)) +
         "\n\tMax difference:                   " + 
             str(round(self.max,2)) +
         "\n\tAvg difference:                   " +
              str(round(self.total/self.count,2)) +
         "\n\tMAE:                              " +
              str(round(self.absTotal/self.count,2)) +
         "\n\tMSE:                              " + 
              str(round(self.sumObservedPredictedDiffSquared/self.count,2)) +
         "\n\tRMSE:                             " + 
              str(round(math.sqrt(
                      self.sumObservedPredictedDiffSquared/self.count),2)))
        
#helper method to remove trailing 0's from string
def removeTrailing( numberAsString  ):
    return numberAsString.rstrip('0').rstrip('.')

############################ POPULAR BMR EQUATIONS ###########################
# Specifically look at equations that consider weight, height, age and gender
# this is because our dataset does not include data on lean mass of subjects.
# Thus equations like Katch-Mccardle and cunningham cannot be compared to.

# Calulcates a subjects TDEE using harris benedict equation.
# Harris benedict equation is a formula that uses BMR and applies 
# an activity level factor to determine TDEE. Built using measurements 
#taken with indirect calorimetry obtained in 239 normal subjects in 1918.
def getOriginalHarrisBenedict( subject ):  
    if subject.isMale():
        return (66 + ( 6.2 * subject.weightPounds ) +
                ( 12.7 * subject.heightInches ) - (6.76 * subject.age  ))
    else: ## subject is female 
        return (655.1 + ( 4.35 * subject.weightPounds ) +
                ( 4.7 * subject.heightInches ) - (4.7 * subject.age  ))
   
# In 1984 Roza and Shizgai revised the harris benedict equation. This 
# equation is considered more accurate than its predecessor but both 
# are still commonly used 
def getRevisedHarrisBenedict( subject ):    
    if subject.isMale():
        return (88.362 + ( 13.397 * subject.getWeightKg() ) +
                ( 4.799 * subject.getHeightCm() ) - (5.677 * subject.age  ))
    else: ## subject is female 
        return (447.593 + ( 9.247 * subject.getWeightKg() ) +
                ( 3.098 * subject.getHeightCm() ) - (4.33 * subject.age  ))
        
#Calculates REE. 498 Individuals were studied and REE was measured by indirect
#calorimetry. Multiple-regression analyses were employed to derive 
#relationships between REE and weight, height, and age.
def getMifflinStJeor( subject ):
    if subject.isMale():
        return ( (10 * subject.getWeightKg()) +
                (6.25 * subject.getHeightCm()) - (5 * subject.age) + 5  )
    else: ## subject is female 
        return ( (10 * subject.getWeightKg()) +
                (6.25 * subject.getHeightCm()) - (5 * subject.age) - 161  )


# The Owen equation (1986/87) for men was based on a sample of 60 subjects
# aged 18 – 82 years. The women’s equation from 44 women aged 18 – 65 years
def getOwen( subject ):
    if subject.isMale():
        return 879 + ( 10.2 * subject.getWeightKg() )
    else: ##subject is female
        return 795 + ( 7.2 * subject.getWeightKg() )

# Developed using data from the Schofield study  n = 11 000 (included men,
# women, and children) Included healthy adults of varying weights,
# heights, and ages. Multiethnic cohort; included a large number
# of Italian participants   
def getWhoFaoUnu( subject ):
    if subject.isMale():
        if subject.age >= 18 and subject.age <= 30:
            return ( (15.4 * subject.getWeightKg() ) -
                    ( 27 * subject.getHeightMeters() ) + 717)
        elif subject.age >= 31 and subject.age <= 60:
            return ( (11.3 * subject.getWeightKg() ) +
                    ( 16 * subject.getHeightMeters() ) + 901)
        elif subject.age > 60 :
            return ( (8.8 * subject.getWeightKg() ) +
                    ( 1128 * subject.getHeightMeters() ) - 1071)
    else: ##subject is female 
        if subject.age >= 18 and subject.age <= 30 :
            return ( (13.3 * subject.getWeightKg() ) +
                    ( 334 * subject.getHeightMeters() ) + 35)
        elif subject.age >= 31 and subject.age <= 60:
            return ( (8.7 * subject.getWeightKg() ) -
                    ( 25 * subject.getHeightMeters() ) + 865)        
        elif subject.age > 60 :
            return ( (9.2 * subject.getWeightKg()) +
                    (637 * subject.getHeightMeters()) - 302 )
            

##############################################################################
            
#LogSmarters model of estimating TDEE 
def getLogSmarter( subject ):
    return LogSmarter.estimate(
            subject.heightInches,
            subject.weightPounds,
            subject.age,
            subject.isMale(),
            subject.getActivityMultiplier())
            

# Returns a list of objects that contain different estimates of TDEE 
# for a given subject. 
def buildEnergyExpenditureResults( subjectList ):
    results = []
    for subject in subjectList:
        results.append( SubjectEnergyResults(subject) )
    return results            
  
# Calculates min max and average difference for estimation techniques from
# true measure of TDEE for a subject 
def testAndCompareModels( resultList ):
    
    ###### ADD VARIABLES TO CALCULAE R^2
    originalHarrisManager = EnergyComparisonResult("Original Harris Benedict")
    revisedHarrisManager = EnergyComparisonResult("Revised Harris Benedict")
    mifflinStJeorManager = EnergyComparisonResult("Mifflin St Jeor")
    owenManager = EnergyComparisonResult("Owen")
    whoFaoUnuManager = EnergyComparisonResult("Who Fao Unu")
    logSmarterManager = EnergyComparisonResult("LogSmarter")
    
    for result in resultList:
        #calculate differences observed in estimate from actual 
        originalHarrisManager.updateForNewSubject( 
                result.originalHarrisBenedict , result.trueTDEE  )

        revisedHarrisManager.updateForNewSubject(  
                result.revisedHarrisBenedict , result.trueTDEE )

        mifflinStJeorManager.updateForNewSubject( 
                result.mifflinStJeor , result.trueTDEE )
        
        owenManager.updateForNewSubject( 
                result.owen , result.trueTDEE )
        
        whoFaoUnuManager.updateForNewSubject( 
                result.whoFaoUnu , result.trueTDEE )
        
        logSmarterManager.updateForNewSubject( 
                result.logSmarter , result.trueTDEE )

    # output
    print( originalHarrisManager )
    print( revisedHarrisManager )
    print( mifflinStJeorManager )
    print( owenManager )
    print( whoFaoUnuManager )
    print( logSmarterManager )
    return


#Exports errors from different extimation techniques to CSV
def exportResultsAndErrors( energyResultsList ):
    
    #### SORT BY ONES WHERE HARRIS BENEDICT BEATS LS BY MOST
    sortedResultsList = sorted( energyResultsList, key=lambda result:
         abs(result.trueTDEE - result.logSmarter) - abs(result.trueTDEE - result.revisedHarrisBenedict), reverse=True)
    with open('data/error.csv' , 'w', newline='' ) as writeFile:
        writer = csv.writer( writeFile )
        rowList = []
        colHeaders = [ "subjNum","TDEE",
                       "originalHarris","originalHarrisError",
                       "revisedHarris","revisedHarrisError",
                       "whoFaoUnu","whoFaoUnu",
                       "owen","owenError",      
                       "mifflinStJeor","mifflinStJeorError",
                       "logSmarter","logSmarterError",
                       "Sex","Age","HeightInches","WeightPounds",
                       "bmi", "activityLevel"]
        rowList.append( colHeaders )
        # Sort list with higher LS errors at top, want to find demographic  
        # that we are overestimating for 
        for result in sortedResultsList:
            errorRow = result.toErrorRow()
            # sort by rows where LSDiff > RevisedHarrisDiff
            harrisDiffLS = abs(result.trueTDEE - result.logSmarter) - abs(result.trueTDEE - result.revisedHarrisBenedict)  
            errorRow.append(harrisDiffLS)
            rowList.append(errorRow)
         
           
        writer.writerows( rowList )
        writeFile.close()
    
#############################   MAIN     #####################################
def main():
    subjectList = cleaner.cleanSubjectData()
    subjectResultsList = buildEnergyExpenditureResults( subjectList )
    
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Test-Model)>").lower().strip()
        if userInput == '/help':
            print("\n" +
                  " /tdeeData        =>\tPrint tdee result dataset\n"+
                  " /bmrData         =>\tPrint bmr result dataset\n"+
                  " /compare         =>\tPrint TDEE estimation comparison\n"+
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
            testAndCompareModels(subjectResultsList)
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