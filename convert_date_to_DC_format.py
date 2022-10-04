#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 05:55:20 2022

@author: bclaridge
"""

import re
import pandas as pd


 ## SET UP FUNCTION THAT TRANSFORMS COMMON COLLECTION DATE FORMATS
 ## TO MACHINE READABLE
 ##
def convert_dates(dataframe_col): 
    """This function takes in a pandas column with either
    typical insect label dates with the months as roman numerals 
    or the first three letters of the month. It returns a new column named
    "eventDate" with the dates formatted as 2022-12-25 which is the correct
    Darwin Core format. The new column is not automatically added to the 
    original dataframe.    
    """
    
    ## CONVERT INPUT COLUMN WHICH IS A SERIES TO A PD DATAFRAME
    dataframe_col = pd.DataFrame(dataframe_col)
    
    ## CONVERT COLUMN ['columnname'] into a list which is easier to deal with
    column_name = dataframe_col.columns.values.tolist()
    empty = ""
    column_name = empty.join(column_name)
    
    ## SET UP NEEDED VARIABLES
    month_RR = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii',
            'ix', 'x', 'xi', 'xii']
    month_CAPS= ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    month_lower = [x.lower() for x in month_CAPS]
    month_Cap = [x.capitalize() for x in month_lower]

    ##CONVERT ODD MONTHS IN RR
    dataframe_col[column_name].replace(regex=month_CAPS, value=month_RR, inplace=True)
    dataframe_col[column_name].replace(regex=month_lower, value=month_RR, inplace=True)
    dataframe_col[column_name].replace(regex=month_Cap, value=month_RR, inplace=True)
    
    ## TURN - into | before other dashes are added
    dataframe_col[column_name].replace(regex="-", value="/", inplace=True)
    ## REPLACE WHITESPACE WITH DOTS
    dataframe_col[column_name].replace(regex=" ", value=".", inplace=True)
 
   
    ## Split DATE into day, month, year
    day = []
    month = []
    year = []
    for index, row in dataframe_col.iterrows():
    ### NEED TO ADD MORE TO REGEX
        match = re.search("[0-9][0-9]\.|[0-9]\.|[0-9]*/[0-9][0-9]", row[column_name])
        if match != None:
            day.append(match.group())
        else:
            day.append(None)
    
    for index, row in dataframe_col.iterrows():
        ## NEED TO ADD MORE REGEX
        match = re.search("[a-zA-Z][a-zA-Z]*", row[column_name])
        if match != None:
            month.append(match.group())
        else:
            month.append(None)

        
    for index, row in dataframe_col.iterrows():
            
        match = re.search("[0-9][0-9][0-9][0-9]*", row[column_name])
        if match != None:
            year.append(match.group())
        else:
            year.append(None)
    
    dataframe_col['Day'] = day
    dataframe_col['Month'] = month
    dataframe_col['Year'] = year
    
    
    dataframe_col['Day'].replace(regex="\.", value="", inplace=True)
    dataframe_col['Month'].replace(regex="\.", value="", inplace=True)
    dataframe_col['Year'].replace(regex="\.", value="", inplace=True)
    
    dataframe_col['eventDate'] = dataframe_col['Year'] + "-" + dataframe_col['Month'] + "-" + dataframe_col['Day']

    dataframe_col['eventDate'].replace(regex="xii", value="12", inplace=True)
    dataframe_col['eventDate'].replace(regex="xi", value="11", inplace=True)
    dataframe_col['eventDate'].replace(regex="ix", value="09", inplace=True)
    dataframe_col['eventDate'].replace(regex="x", value="10", inplace=True)
    dataframe_col['eventDate'].replace(regex="ix", value="09", inplace=True)
    dataframe_col['eventDate'].replace(regex="vii", value="07", inplace=True)
    dataframe_col['eventDate'].replace(regex="vi", value="06", inplace=True)
    dataframe_col['eventDate'].replace(regex="iv", value="04", inplace=True)
    dataframe_col['eventDate'].replace(regex="v", value="05", inplace=True)
    dataframe_col['eventDate'].replace(regex="iii", value="03", inplace=True)
    dataframe_col['eventDate'].replace(regex="ii", value="02", inplace=True)
    dataframe_col['eventDate'].replace(regex="i", value="01", inplace=True)
    
    return dataframe_col['eventDate']