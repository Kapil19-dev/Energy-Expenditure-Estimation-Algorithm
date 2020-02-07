# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""


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

#
def getMifflinStJeor( subject ):
       if( subject.isMale() ):
        return ()
    else: ## subject is female 
        return (655.1 + ( 4.35 * subject.weightPounds ) +
                ( 4.7 * subject.heightInches ) - (4.7 * subject.age  ))


def getKatchMcArdle(subject):
    return 


################# ADD OTHER TDEE ESTIMATION EQUATIONS FROM ARTICLE ##########



def main():
    print("Hello World from Test-Model!")
    
##Tell python to run main function 
if __name__ == "__main__":
    main()