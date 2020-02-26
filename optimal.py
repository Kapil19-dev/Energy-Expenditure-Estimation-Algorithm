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
    
    for error in errors:
        print( error )
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