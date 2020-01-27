# -*- coding: utf-8 -*-
"""
Ryan Lefebvre 1/26/2020
"""
import pandas as pd

# opens raw data.csv and 'cleans' the data so it 
# can be used for analysis to create energy expenditure 
# estimation model
def cleanData():
    rawData = pd.read_csv("data/DLW_TDEE_DATA.csv")
    # only 767 rows of data but read_csv returns 1467 rows
    # drop other 700 rows + 1 row for headers to only retain 
    # rows of interest
    rawData.drop( rawData.tail(701).index ,inplace=True )

def main():
    cleanData()
    
##Tell python to run main function 
if __name__ == "__main__":
    main()