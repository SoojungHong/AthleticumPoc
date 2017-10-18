# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:36:05 2017

@author: a613274

Data cleaning & Feature engineering for nonlinear regression model 
to forecast the sales and margin 
sales forecast =~ (apprx.) past avg sales + weather forcast + visitor flow (recent months) + season factor (if product is sensitive to season) 

"""


#------------------------
# import libraries 
#------------------------
import csv
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


#----------------------------------------------
# function : transform csv file to dataframe
#----------------------------------------------
def readAsDataframe(fileName): 
    #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
    #file = filePath + fileName
    file = atosFilePath + fileName 
    
    #if the read row contains error, throw error 
    df = pd.read_csv(file, error_bad_lines=False)
    df.info()
    print(df.head(10))
    return df
    
     
#----------------------------------------------
# function : transform tsv file to dataframe
#----------------------------------------------
def readTsvAsDataframe(fileName):
    #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
    #file = filePath + fileName
    file = atosFilePath + fileName 
    
    #read .csv file using tab separator, if the read row contains error, throw error 
    df = pd.read_csv(file, error_bad_lines=False, sep="\t")
    return df
   

#-----------------------------
# Test : Read one sales file
#-----------------------------
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
sales = readAsDataframe(salesFile) 

#-----------------------------------------
# Read all sales files (201212 - 201705)
#-----------------------------------------
startYear = 2012
endYear = 2017

years = range(2012, 2018)
years
 
month_in_2012 = range(12, 13)
month_in_2012

month_in_general = range(1, 13)
month_in_general

month_in_2017 = range(1, 6)
month_in_2017


for y in years : 
    if y == 2012 : 
        salesFile = 'factSalesTransactions_' + str(startYear) + '12' + '.csv'
        print(salesFile)
    else :     
        if y == 2017 :
            for m in month_in_2017 : 
                if(m < 10) :
                    salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                    print(salesFile)
                else : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                    print(salesFile)
        else :
            for m in month_in_general : 
                if(m < 10) : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                    print(salesFile)
                else : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                    print(salesFile)
                