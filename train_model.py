# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""

import clean_data as cleaner 
import pandas as pd
import matplotlib.pyplot as plt  
from matplotlib.pyplot import pause
from sklearn.linear_model import LinearRegression
from sklearn import metrics, linear_model
from sklearn.model_selection import train_test_split
import seaborn as seabornInstance


def getLogSmarterModel(regressor):
    intercept = str( round( (regressor.intercept_)[0] , 2 ) )
    maleGenderCoef = str(round((regressor.coef_)[0][0]*2,2))
    coefs = list(map( lambda coef: str(round(coef,2)) , (regressor.coef_)[0]))
    print("\n\t\tTDEE(M) = "
          "\n\t\t       (" + str( intercept ) + ")         + "
          "\n\t\t       (" + maleGenderCoef + "  * SEX)    +" 
          "\n\t\t       (" + coefs[1] + "   * AGE)    +"
          "\n\t\t       (" + coefs[2] + "  * HEIGHT) +"
          "\n\t\t       (" + coefs[3] + "   * WEIGHT) +"
          "\n\t\t       (" + coefs[4] + " * PALCAT) +")
    print("\n\t\tTDEE(F) = " 
          "\n\t\t       (" + str( intercept ) + ")         + "
          "\n\t\t       (" + coefs[0] + ")           +" 
          "\n\t\t       (" + coefs[1] + "   * AGE)    +"
          "\n\t\t       (" + coefs[2] + "  * HEIGHT) +"
          "\n\t\t       (" + coefs[3] + "   * WEIGHT) +"
          "\n\t\t       (" + coefs[4] + " * PALCAT) +")   

#builds the model and returns a trained linear regression object 
# for the model 
def buildModel():
    rawData = cleaner.getRawDataAsPandas()
    #Convert Palcat  and sex from string to number 
    rawData['PALCAT'] = list(map(cleaner.getActivityLevelNumVal,
           rawData['PALCAT']))
    rawData['SEX'] = list(map(cleaner.genderAsNumeric,
           rawData['SEX']))
    #need to deal with catagorical variables         
    x = rawData[[
            'SEX',
            'AGE',
            'HEIGHT',
            'WEIGHT',
            "PALCAT"
            ]] 
    # and response 
    y = rawData[['TDEE']]
    #split data into train and test
    regressor = LinearRegression()
    #Regr coefficients
    regressor.fit(x, y)
    return regressor
    
#displays historgram of TDEE distribution 
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
    regressor = buildModel()
    rawData = cleaner.getRawDataAsPandas()
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Train-Model)>").lower().strip()
        if userInput == '/help':
            print("\n\t/model\t=>\tLogSmarter's estimation model"
                  "\n\t/dist \t=>\tHistogram of observed TDEE"
                  "\n\t/quit \t=>\tEnd script" )
        
        # Plots
        elif userInput == "/model":
            print("\tLogSmarter TDEE Estimation Model:  ")
            getLogSmarterModel(regressor)
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