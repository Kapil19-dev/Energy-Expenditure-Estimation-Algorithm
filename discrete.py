# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:14:45 2020

@author: Ryan
"""

import clean_data as cleaner 
import test_model as tester 
import classes as classes

# list of stat managers is needed by managers to build bucket keys
managers = []
# discrete dict is needed to find optimal equation once we hash into the
# bucket mapping using the bucket key for a subject 
discreteDict = {}

# Finds the optimal equation for a subject based on the bucket that they fall 
# into. This helper function is used to access the discrete model 
def getDiscrete( subject ):
   bucketKey = buildBucketKey(subject)
   optimalEquation = discreteDict[bucketKey]
   result = classes.SubjectEnergyResults(subject)
   return result 

##########################  BUILD MODEL #####################################
# builds bucket mapping for the  optimal equation and updates global
# variables with information about the discrete model
def buildBucketMapping():
    # Get Subjects and statistics ( Need stats for IQR for buckets)
    subjects = cleaner.cleanSubjectData()
    global managers
    managers = cleaner.calculateStats( subjects , False )
    managers = list(filter(lambda man:  man.name != "TDEE" , managers) )
    # get EE estimate results of subjects
    results = tester.buildEnergyExpenditureResults(subjects)
    # get list of errors between EE estimates and true TDEE
    errors = tester.testAndCompareModels(results, False)
    # build buckets to discrete equation form list of errors
    buckets = getBucketDictionary( subjects )
    #calculate discrete equation for each bucket 
    #final reuslt is mapping from bucket --> equation
    global discreteDict
    discreteDict = buildDiscreteDict(buckets)
        
    #test getting optimal 
    for subject in subjects:
        print( str(getDiscrete(subject) ))
############################################################################## 
    

##########################  BUCKET METHODS ###################################  
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
        errors = tester.testAndCompareModels(subjResults , False)
        discreteName = min(errors, key=lambda err: err.getRMSE()).techniqueName
        #mapping from bucket -> discrete eq
        discreteDict[bucketKey] =  discreteName
    return discreteDict
            
##############################################################################  
    
    
    
#############################   MAIN     #####################################    
# Uses results form building initial model and errors from comparing to 
# existing models to create a discretized model for estimating energy 
# expenditure 
def main():
    buildBucketMapping()
    print("For list of commands '/help'")
    while( False ):
        userInput = input("(discrete)>").lower().strip()
        if userInput == '/help':
            print("\n\t/model   \t=>\tLogSmarter's estimation model"
                  "\n\t/dist    \t=>\tHistogram of observed TDEE"
                  "\n\t/optimal \t=>\tMaps buckets -> equations"
                  "\n\t/quit    \t=>\tEnd script" )
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