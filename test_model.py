# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""

import clean_data

# Calulcates a subjects TDEE using harris benedict equation.
# Harris benedict equation is a formula that uses BMR and applies 
# an activity level factor to determine TDEE 
def getRevisedHarrisBenedict( subject ):
    
    tdee = 0
    
    if( subject.isMale() ):
        return (66 + ( 6.2 * subject.weightPounds ) +
                ( 12.7 * subject.heightInches ) - (6.76 * subject.age  ))
    else: ## subject is female 
        return (655.1 + ( 4.35 * subject.weightPounds ) +
                ( 4.7 * subject.heightInches ) - (4.7 * subject.age  ))

#Calculates REE. Individuals were studied and REE was measured by indirect
#calorimetry. Multiple-regression analyses were employed to drive 
#relationships between REE and weight, height, and age 
def getMifflinStJeor( subject ):
       if( subject.isMale() ):
        return ()
    else: ## subject is female 
        return (655.1 + ( 4.35 * subject.weightPounds ) +
                ( 4.7 * subject.heightInches ) - (4.7 * subject.age  ))




################# ADD OTHER TDEE ESTIMATION EQUATIONS FROM ARTICLE ##########



def main():
    print("Hello World from Test-Model!")
    
##Tell python to run main function 
if __name__ == "__main__":
    main()