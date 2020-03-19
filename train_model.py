# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import matplotlib.pyplot as plt  
from matplotlib.pyplot import pause
from sklearn.ensemble import RandomForestRegressor
import seaborn as seabornInstance
import clean_data as cleaner 
import equations as equations
import helper as helpers
import _pickle 


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
    y = rawData['TDEE'] 
    #split data into train and test
    regressor = RandomForestRegressor(n_estimators=200, random_state=0) 
    #Regr coefficients
    regressor.fit(x, y.ravel())
    return regressor

# returns an estimated TDEE using the LogSmarter model 
def estimate(heightInches, weightPounds, ageYears, isMale, palMult ):
    print( str(helpers.genderAsNumeric( helpers.getGenderString(isMale) ) ))
    print( str(palMult))
    subjectData = [[helpers.genderAsNumeric( helpers.getGenderString(isMale) ),
                   ageYears, heightInches, weightPounds, palMult ]]
    estimate = regressor.predict(subjectData)[0]
    return estimate

#Helper method for estimate that takes a subject as a param. Used as param for
# creating subject energy results class instances so they know how to calc LS 
# EE estimates
def getLogSmarter(subject):
    return estimate( subject.heightInches,
                     subject.weightPounds,
                     subject.age,
                     subject.isMale(),
                     subject.getActivityMultiplier())

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
    

# loads the model from the pickled file to avoid re training
def loadPickledModel():    
    with open("data/model.pkl",'rb') as file:
        return _pickle.load(file)

# uses pickle to export the model to a file 
def exportModel():
    with open("data/model.pkl",'wb') as file:
        _pickle.dump(regressor,file)

########################## GLOBAL REGRESSOR ##################################
# making the regressor gloabl improves run time because this way model is only 
# built one time during the execution of the script
regressor = loadPickledModel()
equations.getLogSmarter = getLogSmarter

##############################################################################
        
#############################   MAIN     #####################################
def main():
    rawData = cleaner.getRawDataAsPandas()
    print("For list of commands '/help'")
    while( True ):
        userInput = input("(Train-Model)> ").lower().strip()
        if userInput == '/help':
            print("\n\t/model   \t=>\tLogSmarter's estimation model",
                  "\n\t/export   \t=>\tDump RFR model with pickle",
                  "\n\t/dist    \t=>\tHistogram of observed TDEE"
                  "\n\t/optimal \t=>\tMaps buckets -> equations"
                  "\n\t/quit    \t=>\tEnd script" )
        # Plots
        elif userInput == "/model":
            print("\tLogSmarter TDEE Estimation Model:  ")
            print("\t\t:estimate( 69, 190, 20, True, 1.725 ) = " + 
                   str( estimate( 69, 190, 20, True, 1.725 ))) 
        elif userInput == "/export":
            print("\tDumping model with pickle  ")
            exportModel()
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