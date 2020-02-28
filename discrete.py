# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:14:45 2020

@author: Ryan
"""

import clean_data as cleaner 
import test_model as tester 
import classes as classes

##########################  TEST MODEL #####################################
# Compares the accuracy of the discrete model to the accuracy of other models
# used in these scripts for estimating EE. Prints results to console
def compareDiscrete():
    resultsList = tester.getSubjectResultsList()
    discreteManager = classes.EnergyComparisonResult("discrete")
    for result in resultsList:
        result.discrete = getOptimalForDiscrete(result.subject)
        discreteManager.updateForSubjectResult(result)
    modelManagers = tester.testAndCompareModels( resultsList )
    modelManagers.append( discreteManager )
    for manager in modelManagers:
        print( manager )
        
############################################################################## 
    
##########################  BUCKET METHODS ###################################  
# builds bucket mapping for the  optimal equation and updates global
# variables with information about the discrete model
def buildBucketMapping():
    # Get Subjects and statistics ( Need stats for IQR for buckets)
    subjects = cleaner.getSubjects()
    global managers
    managers = cleaner.calculateStats( subjects , False )
    #Filter out manager for TDEE
    managers = list(filter(lambda man:  man.name != "TDEE" , managers) )
    # build buckets to discrete equation form list of errors
    buckets = getBucketDictionary( subjects )
    #calculate discrete equation for each bucket 
    #final reuslt is mapping from bucket --> equation
    global discreteDict
    discreteDict = buildDiscreteDict(buckets)
    
# Helper method for creating keys for the bucket dictionary.
# Uses managers getBucket method to build a bucket key 
def buildBucketKey( subject ):
    bucketKey =""
    for manager in managers:
        bucketKey += manager.getBucketForSubject(subject)+"_"
    return bucketKey

# Parses a bucket key and prints meaningful information that is true 
# about all subjects in that bucket 
def printBucketKey( key ):
    splitKey = key.split("_")
    print("---------------------------------")
    for key in splitKey :
        parsed = key.split("-")
        if len(parsed) > 1:
            print(parsed[1].upper() + ": " + parsed[0].lower()  )

# returns a dictionary where keys are properties that describe a bucket and 
# the values are list of subjects who fall in that bucket 
def getBucketDictionary( subjects ):    
    ## mapping from bucketKey -> list of usbjects in bucket 
    bucketDict = {}
    
    for subject in subjects:
        bucketKey = bucketKey = buildBucketKey(subject )
        if not bucketKey in bucketDict.keys():
            bucketDict[bucketKey] = []
        bucketDict[bucketKey].append(subject)
        
    return bucketDict

# Helps build discretized model for estimating EE. Does this by 
# mapping from bucket to discrete equation. Returns a dictionary where keys
# are bucket keys and values are keys for which equation to use 
def buildDiscreteDict(buckets):
    discreteDict = {}
    for bucketKey in buckets:
        subjectsInBucket = buckets[bucketKey]
        subjResults = tester.buildEnergyExpenditureResults(subjectsInBucket)
        errors = tester.testAndCompareModels(subjResults)
        discreteName = min(errors, key=lambda err: err.getRMSE()).techniqueName
        #mapping from bucket -> discrete eq
        discreteDict[bucketKey] =  discreteName
    return discreteDict
            
##############################################################################  
    
########################### BUILD DISCRETE #################################
# Finds the optimal equation for a subject based on the bucket that they fall 
# into. This helper function is used to access the discrete model 
def getOptimalForDiscrete( subject ):
   bucketKey = buildBucketKey(subject)
   optimalEquation = discreteDict[bucketKey]
   result = classes.SubjectEnergyResults(subject)
   estimate = getattr( result , optimalEquation )
   return estimate
# list of stat managers is needed by managers to build bucket keys
managers = []
# discrete dict is needed to find optimal equation once we hash into the
# bucket mapping using the bucket key for a subject 
discreteDict = {}
# init managers and discretDict
buildBucketMapping()
##############################################################################

########################### SUGGESTION #######################################

def recommendSurplus(subject, tdee):
    return 0 #temp

def recommendDeficit(subject, tdee):
    return 0 #temp 

##############################################################################

#############################   MAIN     #####################################    
# Uses results form building initial model and errors from comparing to 
# existing models to create a discretized model for estimating energy 
# expenditure 
def main():
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Discrete)> ").lower().strip()
        if userInput == '/help':
            print("\n\t/buckets \t=>\tPrint buckets with optimal equation"
                  "\n\t/compare \t=>\tCompare discrete model to others"
                  "\n\t/quit    \t=>\tEnd script" )
        elif userInput == "/compare":
            compareDiscrete()
        elif userInput == "/buckets":
            bucketCount = 1
            for bucket,equation in discreteDict.items():
                print( "#" + str(bucketCount) + " " + bucket +"\n")
                print("\t"+equation+"\n")
                bucketCount+=1  
        # utility   
        elif userInput == "/quit":
            print("\tTerminating Script  ")
            break
        else:
            print("\tFor list of commands:   '/help'")
            print("\t\tInvalid Input:  " + userInput)

if __name__ == "__main__":
    main()

##############################################################################