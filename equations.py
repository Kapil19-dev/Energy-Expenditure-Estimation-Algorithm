# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:03:41 2020

@author: Ryan
"""

############################ POPULAR BMR EQUATIONS ###########################
# Specifically look at equations that consider weight, height, age and gender
# this is because our dataset does not include data on lean mass of subjects.
# Thus equations like Katch-Mccardle and cunningham cannot be compared to.

# Calulcates a subjects TDEE using harris benedict equation.
# Harris benedict equation is a formula that uses BMR and applies 
# an activity level factor to determine TDEE. Built using measurements 
#taken with indirect calorimetry obtained in 239 normal subjects in 1918.
def getOriginalHarrisBenedict( subject ):  
    if subject.isMale():
        return (66 + ( 6.2 * subject.weightPounds ) +
                ( 12.7 * subject.heightInches ) - (6.76 * subject.age  ))
    else: ## subject is female 
        return (655.1 + ( 4.35 * subject.weightPounds ) +
                ( 4.7 * subject.heightInches ) - (4.7 * subject.age  ))
   
# In 1984 Roza and Shizgai revised the harris benedict equation. This 
# equation is considered more accurate than its predecessor but both 
# are still commonly used 
def getRevisedHarrisBenedict( subject ):    
    if subject.isMale():
        return (88.362 + ( 13.397 * subject.getWeightKg() ) +
                ( 4.799 * subject.getHeightCm() ) - (5.677 * subject.age  ))
    else: ## subject is female 
        return (447.593 + ( 9.247 * subject.getWeightKg() ) +
                ( 3.098 * subject.getHeightCm() ) - (4.33 * subject.age  ))
        
#Calculates REE. 498 Individuals were studied and REE was measured by indirect
#calorimetry. Multiple-regression analyses were employed to derive 
#relationships between REE and weight, height, and age.
def getMifflinStJeor( subject ):
    if subject.isMale():
        return ( (10 * subject.getWeightKg()) +
                (6.25 * subject.getHeightCm()) - (5 * subject.age) + 5  )
    else: ## subject is female 
        return ( (10 * subject.getWeightKg()) +
                (6.25 * subject.getHeightCm()) - (5 * subject.age) - 161  )


# The Owen equation (1986/87) for men was based on a sample of 60 subjects
# aged 18 – 82 years. The women’s equation from 44 women aged 18 – 65 years
def getOwen( subject ):
    if subject.isMale():
        return 879 + ( 10.2 * subject.getWeightKg() )
    else: ##subject is female
        return 795 + ( 7.2 * subject.getWeightKg() )

# Developed using data from the Schofield study  n = 11 000 (included men,
# women, and children) Included healthy adults of varying weights,
# heights, and ages. Multiethnic cohort; included a large number
# of Italian participants   
def getWhoFaoUnu( subject ):
    if subject.isMale():
        if subject.age >= 18 and subject.age <= 30:
            return ( (15.4 * subject.getWeightKg() ) -
                    ( 27 * subject.getHeightMeters() ) + 717)
        elif subject.age >= 31 and subject.age <= 60:
            return ( (11.3 * subject.getWeightKg() ) +
                    ( 16 * subject.getHeightMeters() ) + 901)
        elif subject.age > 60 :
            return ( (8.8 * subject.getWeightKg() ) +
                    ( 1128 * subject.getHeightMeters() ) - 1071)
    else: ##subject is female 
        if subject.age >= 18 and subject.age <= 30 :
            return ( (13.3 * subject.getWeightKg() ) +
                    ( 334 * subject.getHeightMeters() ) + 35)
        elif subject.age >= 31 and subject.age <= 60:
            return ( (8.7 * subject.getWeightKg() ) -
                    ( 25 * subject.getHeightMeters() ) + 865)        
        elif subject.age > 60 :
            return ( (9.2 * subject.getWeightKg()) +
                    (637 * subject.getHeightMeters()) - 302 )
            

##############################################################################