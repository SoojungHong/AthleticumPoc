# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:03:26 2017

@author: a613274

@About: Selecting store for Poc
"""
#----------------------
# Import libraries 
#----------------------
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
 
    
#--------------------------
# Read Store information
storeFile = "dimStore.csv"
stores = readAsDataframe(storeFile)
stores.info()
stores['StoreSizeSqm'] #Finding - There is no information about the size of store
stores['StoreCodeName']
#stores['PathName01'] #Question : no idea what it is
#stores['StoreLedgerAccount'] #Question : no idea what it is 
stores['PathName02'] #region name 
stores['PathName03'] #city name 

                
#---------------------------------------------------------------------------------------------------------------
# Construct dataframe with 'StoreID', 'StoreSizeSqm', 'StoreCodeName', 'PathName02(region)', 'PathName03(city)'
columnNames = ['StoreID', 'StoreSizeSqm', 'StoreCodeName', 'PathName02', 'PathName03']
storesSimplified = stores[columnNames]
storesSimplified

#--------------------------
# Read sales transaction 
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
sales = readAsDataframe(salesFile) 
sales.info()
 
#--------------------------------
# Join storeFilea and salesFile   
joined = pd.merge(storesSimplified, sales, on='StoreID', how='inner')
joined.info()
joined.tail(10)
joined['NetAmount']
#joined['NetPrice'] #same as NetAmount
joinColumnNames = ['StoreID', 'StoreSizeSqm', 'StoreCodeName', 'PathName02', 'PathName03', 'NetAmount']

joinedSimplified = joined[joinColumnNames]
joinedSimplified 

#------------------------------
# per Store, sum of NetAmount
joinedSimplified['sum_values_netamount'] = joinedSimplified.groupby('StoreID')['NetAmount'].transform(np.sum)
joined_withoutDuplicate=joinedSimplified.drop_duplicates(subset=['StoreID', 'StoreSizeSqm', 'StoreCodeName', 'PathName02', 'sum_values_netamount'], keep='first')
print(type(joined_withoutDuplicate))

#sort using NetAmount
joined_withoutDuplicate.sort(['sum_values_netamount'], ascending=False)
joined_withoutDuplicate = joined_withoutDuplicate.sort_values(by=['sum_values_netamount'], ascending=[False])
joined_withoutDuplicate