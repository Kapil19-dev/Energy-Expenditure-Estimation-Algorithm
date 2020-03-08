# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import matplotlib.pyplot as plt  
from matplotlib.pyplot import pause
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import seaborn as seabornInstance
import clean_data as cleaner 
import equations as equations
import helper as helpers


# Builds the model and returns a trained linear regression object 
# for the model 
def buildModel():
    rawData = cleaner.getRawDataAsPandas()
    #Convert Palcat  and sex from string to number 
    rawData['PALCAT'] = list(map(helpers.getActivityLevelNumVal,rawData['PALCAT']))
    rawData['SEX'] = list(map(helpers.genderAsNumeric,rawData['SEX']))
    # want to work with imperial units 
    rawData['HEIGHT'] = list(map(helpers.metersToInches,rawData['HEIGHT']))
    rawData['WEIGHT'] = list(map(helpers.kgToLbs,rawData['WEIGHT']))
    #need to deal with catagorical variables         
    x = rawData[['SEX','AGE','HEIGHT','WEIGHT',"PALCAT"]] 
    # and response 
    y = rawData['TDEE'] # rawData[['TDEE']]
    #split data into train and test
    regressor = RandomForestRegressor(n_estimators=200, random_state=0) #LinearRegression()
    print( x )
    #Regr coefficients
    regressor.fit(x, y.ravel())
    #predictions = regressor.predict(x)
    return regressor

#Helper for getting gender coef for LgoSmarter model
def getGenderCoef(isMale):
    if( isMale == True ):
        return maleGenderCoef
    else:
        return femaleGenderCoef

# returns an estimated TDEE using the LogSmarter model 
def estimate(heightInches, weightPounds, ageYears, isMale, palMult ):
    #prediction = regressor.predict([])
    subjectData = [[helpers.genderAsNumeric( helpers.getGenderString(isMale) ),
                   ageYears, heightInches, weightPounds, palMult ]]
    estimate = regressor.predict(subjectData)[0]
    return estimate
    #return regressor.predict
            #round( 
            #( intercept ) +
            #( ageYears * ageCoef ) +
            #( heightInches * heightCoef ) +
            #( weightPounds * weightCoef ) +
            #( palMult * palCoef ) + 
            #( getGenderCoef(isMale) ),2)

#Helper method for estimate that takes a subject as a param. Used as param for
# creating subject energy results class instances so they know how to calc LS 
# EE estimates
def getLogSmarter(subject):
    return estimate( subject.heightInches,
                     subject.weightPounds,
                     subject.age,
                     subject.isMale(),
                     subject.getActivityMultiplier())

#Prints LogSmarter model to the console in readable format
def getLogSmarterModel():
    print("\n\t\tTDEE(M) = "
          "\n\t\t       (" + str(round(intercept +
                                       maleGenderCoef,2)) + ")          +"
          "\n\t\t       (" + str(round(ageCoef,2)) + "   * AGE)    +"
          "\n\t\t       (" + str(round(heightCoef,2)) + "   * HEIGHT) +"
          "\n\t\t       (" + str(round(weightCoef,2)) + "    * WEIGHT) +"
          "\n\t\t       (" + str(round(palCoef,2)) + " * PALCAT)" )
    
    print("\n\t\tTDEE(F) = " 
          "\n\t\t       (" + str(round(intercept +
                                       femaleGenderCoef,2)) + ")         +" 
          "\n\t\t       (" + str(round(ageCoef,2)) + "   * AGE)    +"
          "\n\t\t       (" + str(round(heightCoef,2)) + "   * HEIGHT) +"
          "\n\t\t       (" + str(round(weightCoef,2)) + "    * WEIGHT) +"
          "\n\t\t       (" + str(round(palCoef,2)) + " * PALCAT)")

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
    
########################## GLOBAL REGRESSOR ##################################
# making the regressor gloabl improves run time because this way model is only 
# built one time during the execution of the script
regressor = buildModel()
#intercept =  (regressor.intercept_)[0] 
#maleGenderCoef = ((regressor.coef_)[0][0])*2
#femaleGenderCoef = (regressor.coef_)[0][0]
#coefs = (regressor.coef_)[0]
#ageCoef = coefs[1]
#heightCoef = coefs[2]
#weightCoef = coefs[3]
#palCoef = coefs[4]
#Update get LogSmarter in equations.py
equations.getLogSmarter = getLogSmarter
##############################################################################
        
#############################   MAIN     #####################################
def main():
    rawData = cleaner.getRawDataAsPandas()
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Train-Model)> ").lower().strip()
        if userInput == '/help':
            print("\n\t/model   \t=>\tLogSmarter's estimation model"
                  "\n\t/dist    \t=>\tHistogram of observed TDEE"
                  "\n\t/optimal \t=>\tMaps buckets -> equations"
                  "\n\t/quit    \t=>\tEnd script" )
        # Plots
        elif userInput == "/model":
            print("\tLogSmarter TDEE Estimation Model:  ")
            print( estimate( 69 , 190, 20 , True, 1.725 ) ) 
           # getLogSmarterModel()
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