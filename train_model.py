# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""

import clean_data as cleaner 
import pandas as pd
import matplotlib.pyplot as plt  
from matplotlib.pyplot import pause
from sklearn import metrics, linear_model
from sklearn.model_selection import train_test_split
import seaborn as seabornInstance

def buildModel():
    rawData = cleaner.getRawDataAsPandas()
    #Convert Palcat from string to number 
    rawData['PALCAT'] = list(map(cleaner.getActivityLevelNumVal,
           rawData['PALCAT']))
    rawData['SEX'] = list(map(cleaner.genderAsNumeric,
           rawData['SEX']))
    #need to deal with catagorical variables         
    x = rawData[[
            "SEX",
            "PALCAT",
            'AGE',
            'HEIGHT',
            'WEIGHT',
            'BMI']]
    # and response 
    y = rawData[['TDEE']]
    #split data into train and test
    regressor = linear_model.LinearRegression()
    #Regr coefficients
    x_train, x_test, y_train, y_test = ( 
            train_test_split(x, y, test_size=0.2, random_state=0 ))
    regressor.fit(x_train, y_train  )
    

    
#displays historgrma of TDEE distribution 
def checkDistribution(rawData):
     plt.figure(figsize=(15,10))
     plt.tight_layout()
     seabornInstance.distplot(rawData['TDEE'])
     anacondaDisplayPlot()
     

#Issues with matplotlib in anaconda environment. Plots will not appear 
# in figure window and if set to appear in the console only appear if 
# a delay is added using pause
def anacondaDisplayPlot():
    pause(1)

#############################   MAIN     ###################################
def main():
    rawData = cleaner.getRawDataAsPandas()
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Train-Model)>").lower().strip()
        if userInput == '/help':
            print("\n\t/model     =>\tLogSmarter's estimation model"
                  "\n\t/dist      =>\tHistogram of observed TDEE"
                  "\n\t/quit      =>\tEnd script" )
        
        # Plots
        elif userInput == "/model":
            print("\tLogSmarter TDEE Estimation Model:  ")
            buildModel()
        elif userInput == "/dist":
            print("\tHistogram of TDEE Distribution:  ")
            checkDistribution(rawData)
        # utility   
        elif userInput == "/quit":
            print("\tTerminating Script  ")
            break
        else:
            print("\tFor list of commands:   '/help'")
            print("\t\tInvalid Input:  " + userInput)
                
######################################################################

    
##Tell python to run main function 
if __name__ == "__main__":
    main()