# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:05:05 2020

@author: Ryan
"""

import math

###########################   CONVERSIONS     ###############################
# converts activity level from string -> num
def getActivityLevelNumVal(activityLevel):
    activityLevel = upperTrim(activityLevel)
    if activityLevel == 'S':
        return 1.2
    elif activityLevel == "LA":
        return 1.375
    elif activityLevel == "A":
        return 1.55
    else:
        return 1.725

#converts gender from string -> num
def genderAsNumeric(gender):
    if upperTrim(gender) == "M":
        return 2
    return 1

#helper method for reutrning the correct gender string of alpha users 
def getGenderString(isMale):
    if isMale == True:
        return "M"
    elif isMale == False:
        return "F"
    else:
        return None 
    

# converts a weight in kg to weight in lbs 
def kgToLbs( weightInKg ):
    return round( weightInKg * 2.2 , 2 )

#converts a weight in lbs to a weight in kg
def lbsToKg( weightInLbs ):
    return round( weightInLbs / 2 , 2 )

#converts a height in meters to a height in lbs
def metersToInches( heightInMeters ):
    return round( heightInMeters * 39.3701 , 2 )

#converts a height in inches to  a height in meters 
def inchesToMeters( heightInInches ):
    return round( heightInInches * 0.0254 , 2 )

#converts a height in inches to cm
def inchesToCm( heightInInches ):
    return round( heightInInches * 2.54 , 2 )

#converts a height in inches to as tring of the same height in ft and inches
def inchesToFeetAndInches( heightInInches ):
    feet =  math.floor( heightInInches / 12 ) 
    inches = math.floor( heightInInches % 12 )
    return str(feet)+"'"+str(inches)+"\""

#converts a number to a string, rounded to dec decimal places
#needed helper for this because I do it alot 
def strRound( number , dec ):
    return str( round( number , dec ) )

##############################################################################
    

######################### STRING FORMATTING ##################################

# helper method for clean data converts string to
# uppercase and trims it allows for only one call to map 
def upperTrim( string ):
    return string.upper().strip()

#helper method to remove trailing 0's from string
def removeTrailing( numberAsString  ):
    return numberAsString.rstrip('0').rstrip('.')

#############################################################################