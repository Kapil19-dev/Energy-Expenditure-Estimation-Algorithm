# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:14:45 2020

@author: Ryan
"""

import clean_data as cleaner 
import test_model as tester 


##########################  BUILD MODEL #####################################
# builds optimal equation and updates global variables with information 
# about the equation 
def build():
    # Get Subjects
    subjects = cleaner.cleanSubjectData()
    # results of subjects
    results = tester.buildEnergyExpenditureResults(subjects)
    # get list of errors 
    errors = tester.testAndCompareModels(results, False)
    # build buckets to optimal equation form list of errors
    buckets = getBucketDictionary( subjects )
    #calculate optimal equation for each bucket 
    # final reuslt is mapping from bucket --> equation
    optimalDict = buildOptimalDict(buckets)
    

##############################################################################   
    

##########################  BUCKET METHODS ###################################  
# Helper method for creating keys for the bucket dictionary.
# Uses managers getBucket method to build a bucket key 
def buildBucketKey( subject , managers ):
    bucketKey =""
    for manager in managers:
        bucketKey += manager.getBucketForSubject(subject)+"_"
    return bucketKey

# Parses a bucket key and prints meaningful information that is true 
# about all usbjects in that bucket 
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
    # first filter out tdee. Wouldn't make sense to have target considered 
    # in buckets
    managers = cleaner.calculateStats( subjects , False )
    managers = list(filter(lambda man:  man.name != "TDEE" , managers) )
    
    ## mapping from bucketKey -> list of usbjects in bucket 
    bucketDict = {}
    
    for subject in subjects:
        bucketKey = bucketKey = buildBucketKey(subject, managers)
        if not bucketKey in bucketDict.keys():
            bucketDict[bucketKey] = []
        bucketDict[bucketKey].append(subject)
        
    return bucketDict

# Builds what I am calling the 'optimal' algorithm. Builds mapping from bucket
# to optimal equation. Returns a dictionary where keys are bucket keys 
# and values are keys for which equation to use 
def buildOptimalDict(buckets):
    optimalDict = {}
    for bucketKey in buckets:
        subjectsInBucket = buckets[bucketKey]
        subjResults = tester.buildEnergyExpenditureResults(subjectsInBucket)
        errors = tester.testAndCompareModels(subjResults , False)
        optimalName = min( errors, key=lambda err: err.getRMSE() ).techniqueName
        #mapping from bucket -> optimal eq
        optimalDict[bucketKey] =  optimalName
    return optimalDict
            
##############################################################################  
    
    
    
#############################   MAIN     #####################################    
# Uses results form building initial model and errors from comparing to 
# existing models to create a discretized model fro estimating energy 
# expenditure 
def main():
    build()
    print("For list of commands '/help'")
    while( False ):
        userInput = input("(Build-Optimal)>").lower().strip()
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