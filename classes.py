# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:25:15 2020

@author: Ryan
"""

import helper
import equations
import math

###############################   CLEAN DATA    ###############################

#Represents an alpha user in our system
class AlphaUser():
    def __init__( self,
                   uid,
                   email,
                   username,
                   sex, 
                   age,
                   heightInches,
                   weightPounds):
        self.uid = uid
        self.email = email
        self.username = username
        self.sex = sex
        self.age = age
        self.heightInches = heightInches
        self.weightPounds = weightPounds 
        self.isAlpha = True

    def isMale(self):
        return self.sex == "M"

    def displayGender(self):
        if self.sex == None:
            return ""
        else:
            return self.sex
        
    def displayWeight(self):
        if self.weightPounds == None:
            return ""
        else:
            return str(self.weightPounds)
        
    def displayAge(self):
        if self.age == None:
            return ""
        else:
            return str(self.age)
        
    def displayHeight(self):
        if self.heightInches == None:
            return ""
        else:
            return str(helper.inchesToFeetAndInches((self.heightInches)))
        
    def __str__(self):
        return ( "User id:  " +
                    str(self.uid).strip() +
                 "\nEmail:    " +
                     str(self.email) +
                 "\nUsername: " +
                     str(self.username) + 
                 "\nSex:      " +
                     self.displayGender() +
                 "\nAge:      " +
                     self.displayAge() +
                 "\nHeight:   " + 
                     self.displayHeight() +
                 "\nWeight:   " +
                     self.displayWeight() +
                 "\n-------------------------------------")
    
#Python class object that represents  
class Subject():
    def __init__( self,
                   subjNum,
                   sex, 
                   age,
                   heightInches,
                   weightPounds,
                   bmi,
                   tdee,
                   activityLevel):
        self.sex = sex
        self.age = round( age , 0 )
        self.heightInches = heightInches
        self.weightPounds = weightPounds
        self.bmi = bmi
        self.tdee = tdee
        self.activityLevel = activityLevel
        self.subjNum = subjNum
        self.isAlpha = False
        
    def isMale(self):
        return self.sex == "M"
    
    def getWeightKg(self):
        return helper.lbsToKg(self.weightPounds)
    
    def getHeightCm(self):
        return helper.inchesToCm(self.heightInches)
    
    def getHeightMeters(self):
        return helper.inchesToMeters( self.heightInches )
    
    def getActivityMultiplier(self):
        return helper.getActivityLevelNumVal(self.activityLevel)
        
    
    def __str__(self):
        return ( "Subject Number: " + str(self.subjNum ) + "\tSex: "+
                str(self.sex) + "\tAge: " + str(self.age) + "\tWeight: "+
                str(self.weightPounds)+ "\tHeight: " +
                str(helper.inchesToFeetAndInches((self.heightInches))) + "\tBMI: "+
                str(self.bmi) + "\tTDEE: " + str(self.tdee) + 
                "\tActivity Level: " + str(self.activityLevel) + "\n" )
        
#Helper class for accumulating and calculating numeric subject stats
class NumericStatManager():
    def __init__(  self,
                   statName, 
                   statUnits,
                   subjPropertyName):
        self.name = statName
        self.min = 0
        self.max = 0
        self.total = 0
        self.reported = 0
        self.units = statUnits 
        self.values = []
        self.subjPropertyName = subjPropertyName
        #q1,q2,q3,IQR
        self.quartiles = ( 0,0,0,0 )
        
    # adds data for a stat to the manager    
    def update( self, subject ):
        value = getattr(subject,self.subjPropertyName)
        if value < self.min or self.min == 0:
            self.min = value
        if value > self.max or self.max == 0:
            self.max = value
        self.total += value
        self.reported += 1
        self.values.append( value )
        self.updateQuartiles()
        
    #returns a tuple 
    def updateQuartiles(self):
        self.values.sort()
        idxOfQ1 = round( self.reported * ( 1/4 ) )
        idxOfQ2 = round( self.reported * ( 2/4 ) )
        idxOfQ3 = round( self.reported * ( 3/4 ) )
        if ( ( idxOfQ1 > -1 and idxOfQ1 < self.reported ) and
             ( idxOfQ2 > -1 and idxOfQ2 < self.reported ) and
             ( idxOfQ3 > -1 and idxOfQ3 < self.reported ) ):
            iqr = round( self.values[idxOfQ3] - self.values[idxOfQ1] )
            self.quartiles = (self.values[idxOfQ1], #Q1
                              self.values[idxOfQ2], #Q2
                              self.values[idxOfQ3], #Q3
                              iqr)
            
    #returns which bucket a value falls into
    # val <= q1 is low
    # q1 < val < q3 is avg 
    # val >= q3 is high
    def getBucketForSubject(self,subj):
        val = getattr(subj,self.subjPropertyName)
        bucket = ""
        q1 = self.quartiles[0]
        q3 = self.quartiles[3]
        if val <= q1:
            bucket = "low"
        elif q1 < val and val < q3:
            bucket = "avg"
        elif val >= q3:
            bucket =  "high"
        return bucket+"-"+self.name
                    
    def __str__(self):
        return("<---"+self.name+"---> " +
         "\n\tMin "+self.name+":                 " +
              str(round(self.min,2)) + " " + self.units +
         "\n\tAvg " +self.name+":                 " +
              str(round(self.total/self.reported,2)) + " " + self.units +
         "\n\tMax " +self.name+":                 " +
              str(round(self.max,2)) + " " + self.units +
          "\n\tQ1:                          " + str(self.quartiles[0])  +
          "\n\tQ2:                          " + str(self.quartiles[1])  +
          "\n\tQ3:                          " + str(self.quartiles[2])  +
          "\n\tIQR:                         " + str(self.quartiles[3]))
    #true if empty
    def isEmpty(self):
        return self.reported == 0 
    
#Helper class for accumulating and calculating catagorical subject stats
class CatagoricalStatManager():
    def __init__(  self,
                   statName,
                   subjPropertyName):
        self.name = statName
        # keeps track of occurences of each catagory in the dataset
        self.catagoryCounts = {}
        self.subjPropertyName = subjPropertyName
        self.reported = 0
        
        
     # helper for building bucket key for subjects   
    def getBucketForSubject(self,subject):
        bucket = getattr(subject,self.subjPropertyName)
        return bucket +"-"+ self.name
        
        
    #updates count of category that value is in and num of reports
    def update( self, subject ):
        value = getattr(subject,self.subjPropertyName)
        if not value in self.catagoryCounts.keys():
            self.catagoryCounts[value] = 0
        self.catagoryCounts[value] += 1
        self.reported += 1 
    
    def __str__(self):
        retStr = "<---"+self.name+"---> "
        if self.isEmpty():
            retStr += "\n NO STATS "
        else:
            for key , value in self.catagoryCounts.items():
                retStr += ( "\n\t Total " + key +  ": " + 
                           helper.strRound( value, 2  ) + "\n\t\t % " + key +
                           ": " + helper.strRound((value/self.reported)*100,2 )+"%")
        return retStr
    
    #true if empty
    def isEmpty(self):
        return self.reported == 0 
    
###############################   TEST RESULTS  ###############################
class SubjectEnergyResults():
    #constructor
    def __init__( self,subject):
        self.subject = subject
        self.subjectID = subject.subjNum
        self.trueTDEE = subject.tdee
        self.logSmarter = 0
        ############## BELOW ARE BMR ESTIMATES #########################
        # TDEE = BMR estimate * activityLevel
        # below is a comprehensive source of all popular estimation methods
        # https://completehumanperformance.com/2013/10/08/calorie-needs/
        self.originalHarrisBenedict = (equations.getOriginalHarrisBenedict( subject ) *
                                       subject.getActivityMultiplier() )
        self.revisedHarrisBenedict = (equations.getRevisedHarrisBenedict( subject ) *
                                      subject.getActivityMultiplier() )
        self.mifflinStJeor = (equations.getMifflinStJeor(subject) *
                              subject.getActivityMultiplier() )
        self.whoFaoUnu = ( equations.getWhoFaoUnu(subject) *
                          subject.getActivityMultiplier() )
        self.owen = equations.getOwen(subject) * subject.getActivityMultiplier() 
        self.optimal = -1

    #converts to string
    def __str__(self):
        return ( "Subject Number: " + str(self.subjectID) + "\n"
                "\n\tTrue TDEE:                " +
                    str(round(self.trueTDEE,0) ) +
                "\n\tLogSmarter:               " +
                    helper.removeTrailing(str(round(self.logSmarter,0))) +
                "\n---------- TDEE ESTIMATES -----------" +
                "\n\tOriginal Harris Benedict: " +
                    helper.removeTrailing(str(round(self.originalHarrisBenedict,0)))+ 
                "\n\tRevised Harris Benedict:  " +
                    helper.removeTrailing(str(round(self.revisedHarrisBenedict,0)))+
                "\n\tMifflin-St Jeor:          " +
                    helper.removeTrailing(str(round(self.mifflinStJeor,0))) +
                "\n\tOwen:                     " +
                    helper.removeTrailing(str(round(self.owen,0))) +
                "\n\tWHO-FAO-UNU:              " +
                    helper.removeTrailing(str(round(self.whoFaoUnu,0))) +
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
                    helper.removeTrailing(str(round(self.logSmarter,0))) +
                "\n---------- BMR ESTIMATES -----------" + 
                "\n\tOriginal Harris Benedict: " +
                    helper.removeTrailing(str(round(self.originalHarrisBenedict / 
                                self.subject.getActivityMultiplier() ,0)))+ 
                "\n\tRevised Harris Benedict:  " +
                    helper.removeTrailing(str(round(self.revisedHarrisBenedict /
                                self.subject.getActivityMultiplier() ,0)))+
                "\n\tMifflin-St Jeor:          " +
                    helper.removeTrailing(str(round(self.mifflinStJeor /
                                self.subject.getActivityMultiplier(),0))) +
                "\n\tOwen:                     " +
                    helper.removeTrailing(str(round(self.owen / 
                                self.subject.getActivityMultiplier(),0))) +
                "\n\tWHO-FAO-UNU:              " +
                    helper.removeTrailing(str(round(self.whoFaoUnu /
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
            self.sumObservedPredictedDiffSquared = 0
            # total number of subjects we've added data for
            self.count = 0

    def getMSE(self):
        return self.sumObservedPredictedDiffSquared/self.count
            
    def getRMSE(self):
        return math.sqrt(self.getMSE())
    
    def getMAE(self):
        return self.absTotal/self.count
        
    #updates min max and avg for a subjects difference from their 
    # true estimate for a given technique 
    def updateForSubjectResult( self, result ):
        estimate = getattr( result, self.techniqueName )
        actual = result.subject.tdee
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
              str(round(self.getMAE(),2)) +
         "\n\tMSE:                              " + 
              str(round(self.getMSE(),2)) +
         "\n\tRMSE:                             " + 
              str(round(self.getRMSE(),2)))