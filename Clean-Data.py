# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd

# helper method for clean data converts string to
# uppercase and trims it allows for only one call to map 
def upperTrim( string ):
    return string.upper().strip()

# opens raw data.csv and 'cleans' the data so it 
# can be used for analysis to create energy expenditure 
# estimation model
def cleanData():
    rawData = pd.read_csv("data/DLW_TDEE_DATA.csv")
    # only 766 rows of data but read_csv returns 1467 rows
    # drop other 701 rows to only retain headers and
    # rows of interest
    rawData.drop( rawData.tail(701).index ,inplace=True )
    #drop columns that are not of interest 
    colsToDrop = [5,7,9,10,11,12,13,14,
                  15,16,17,18,19,20,21,
                  22,23,24,25]
    rawData.drop(rawData.columns[colsToDrop],axis=1,inplace=True)
    #consistent format for column names 
    rawData.columns = map( upperTrim , rawData.columns )
    #consistent with acronym for energy expenditure 
    rawData.rename( columns = {'TEE':'TDEE'} , inplace= True )


def main():
    cleanData()
    
##Tell python to run main function 
if __name__ == "__main__":
    main()