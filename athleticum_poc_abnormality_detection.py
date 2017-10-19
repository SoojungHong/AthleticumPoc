# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:48:48 2017

@author: a613274

@about: Abnormality Detection using Classification
classify binary classes - normal (0), abnormal(1)

1. abnormality type : sales abnormality 
2. abnormality type : seasonal product category abnormality 


Feature df example>> 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Date (YY-MM) ¦ Total Sales (Sum) ¦ Most frequent Product category ¦ Least frequent Product category ¦ Most frequent product category's sale frequency ¦ Lease frequent category's sales frequency ¦ Class
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


#----------------------
# Feature engineering 
#----------------------

#First, construct feature as Date - Most & least frequent product category - class 


"""
-------------------------------------------------------------------------------------------
 Date (YY-MM) ¦ Most frequent Product category ¦ Least frequent Product category ¦ Class
-------------------------------------------------------------------------------------------

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
from random import randint
import datetime as dt




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
    #df.info()
    
    #strip column names 
    df.columns = df.columns.str.strip()

    #print(df.head(10))
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




#-------------------------------------------
# function : convert string to date format
#-------------------------------------------
def convertDate(dateStr): 
    date = dt.datetime.strptime(dateStr, '%Y%m')
    return date



        
#----------------------------------------------------------------------------------------------------------------------------
# Construct dataframe with 'Date', 'Most frequent Product category', 'Least frequent Product category', 'Abnormality Class'
#----------------------------------------------------------------------------------------------------------------------------
columnNames = ['Date', 'Most Frequent Product Category', 'Least Frequent Product Category', 'Abnormality Class']
index = np.arange(0)
featureDF = pd.DataFrame(columns=columnNames, index = index)

# 1. read sales data 
# 2. join with product dimension data 
# 3. count the frequency of purchase per UniverseCode
# 4. Pick the most frequent product category (universe)
# 5. Pick the least frequent product category (universe)


#-----------------------------
# Test : Read one sales file
#-----------------------------
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
sales = readAsDataframe(salesFile) 
sales.info()


dimProduct = 'dimProduct_TSV.csv' #ToDo : Read TSV
#product = readAsDataframe(dimProduct) #ToDo : unclean data
product = readTsvAsDataframe(dimProduct)
product.info()
product.head(5)
product.groupby(['UniverseCodeDesc']).size()

# do a bit of data cleaning 
sales = sales.convert_objects(convert_numeric=True)
sales.columns = sales.columns.str.strip()

product.columns = product.columns.str.strip()
product = product.dropna(subset=['ProductID']) #251550
#product = product.convert_objects(convert_numeric=True)

   
joined = pd.merge(product, sales, on='ProductID', how='inner')
joined.info()
joined.tail(10)


universeGroupBy = joined.groupby(['UniverseCodeDesc']).size() # 10 wintersport
universeGroupBy.keys()[1]
universeGroupBy[1]
# First get nlargest 5, pick which is not N/A
topFive = universeGroupBy.nlargest(5)
topFive 

m = 0
while (topFive.keys()[m].find('N/A') != -1):
    print 'It is N/A'
    m = m + 1
print m#topFive[m]    

universeGroupBy.nsmallest(3)
print(type(universeGroupBy))

# among smallest, which is not N/A
bottomFive = universeGroupBy.nsmallest(5)
bottomFive 

l = 0
while (bottomFive.keys()[l].find('N/A') != -1):
    print 'It is N/A'
    l = l + 1  
print bottomFive.keys()[l]

print bottomFive[l]
print bottomFive.keys()[l]    

universeGroupBy.nsmallest(3)
print(type(universeGroupBy))


# ToDo : Why UniverseCodeDesc is NaN? 
# ToDo : Normalization of the product category (since number of ballsport is bigger than Running for example)
