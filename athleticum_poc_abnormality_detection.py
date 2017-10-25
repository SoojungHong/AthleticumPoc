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



#----------------------------------------------------------
# function : find most frequently purchased product group
#---------------------------------------------------------
def getMostFreqGroup(universeGroupBy): 
    topFive = universeGroupBy.nlargest(5)
    m = 0
    while (topFive.keys()[m].find('N/A') != -1):
        print 'It is N/A'
        m = m + 1
    return topFive.keys()[m]


#----------------------------------------------------------
# function : find least frequently purchased product group
#---------------------------------------------------------
def getLeastFreqGroup(universeGroupBy): 
    bottomFive = universeGroupBy.nsmallest(5)
    l = 0
    while (bottomFive.keys()[l].find('N/A') != -1):
        print 'It is N/A'
        l = l + 1  
    return bottomFive.keys()[l]
    


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
universeGroupBy

test = getMostFreqGroup(universeGroupBy)
test 


test2 = getLeastFreqGroup(universeGroupBy)
test2 



#-------------
# Get month 
#-------------
"""
df.iloc[[2]]

joined 

joined_df = joined.as_matrix()
NROW(joined_df)
joined_df.shape
total_rows=len(df.axes[0])
total_rows
total_cols=len(df.axes[1])
total_cols

i = 1000
joined_df[i]
"""

def getSeasonByMonth(date):
    season = 'spring'
    # get Month 
    #dateInt = int(row['DateID'])
    #print(dateInt)
    dateStr = str(date)
    datee = dt.datetime.strptime(dateStr, "%Y%m")
    #print(datee.month)
    month = datee.month
    if(month > 5 & month < 10) : 
        season = 'summer'
    else: 
        if(month < 3 & month > 10):
            season = 'winter'
    print(season)        
    return season
    # return season 
    
    
#----------------------------------------------
# Join product and Monthly Sales Transaction 
#----------------------------------------------
def getJoinedWithProduct(sales, product):
    """
    dimProduct = 'dimProduct_TSV.csv' #ToDo : Read TSV
    #product = readAsDataframe(dimProduct) #ToDo : unclean data
    product = readTsvAsDataframe(dimProduct)
    product.info()
    product.head(5)
    product.groupby(['UniverseCodeDesc']).size()
    """

    # do a bit of data cleaning 
    sales = sales.convert_objects(convert_numeric=True)
    sales.columns = sales.columns.str.strip()

    product.columns = product.columns.str.strip()
    product = product.dropna(subset=['ProductID']) #251550
    #product = product.convert_objects(convert_numeric=True)
    joined = pd.merge(product, sales, on='ProductID', how='inner')
    
    return joined
    


#----------------------------------------
# Add one row in the feature dataframe 
#----------------------------------------
def setFeature(date, df, featureDF): 
    # product 
    dimProduct = 'dimProduct_TSV.csv' #ToDo : Read TSV
    #product = readAsDataframe(dimProduct) #ToDo : unclean data
    product = readTsvAsDataframe(dimProduct)
    #product.info()
    #product.head(5)
    #product.groupby(['UniverseCodeDesc']).size()
 
    #print(df.iloc[[0]]) #read 0 index row
    """
    zeroIndexRow = df.iloc[[1]] # To Do : Fix this - error intolerant!!
   
    dateInt = int(zeroIndexRow['DateID'])
    #print(dateInt)
    dateStr = str(dateInt)
    datee = dt.datetime.strptime(dateStr, "%Y%m%d")
    #print(datee.month)
    month = datee.month
    #season = getSeasonByMonth(zeroIndexRow)
    """
    
    joined = getJoinedWithProduct(df, product)
    universeGroupBy = joined.groupby(['UniverseCodeDesc']).size() 

    mostfreGrp = getMostFreqGroup(universeGroupBy) 
    leastfreGrp = getLeastFreqGroup(universeGroupBy)
    #print(month)
    #print(mostfreGrp)
    #print(leastfreGrp)
    normality = assignNormalityValue(date, mostfreGrp)
    featureDF = featureDF.append({'Date': date, 'Most Frequent Product Category': mostfreGrp, 'Least Frequent Product Category': leastfreGrp, 'Abnormality Class' : normality}, ignore_index=True)
    return featureDF
    
    
#----------------------------------
# Constructing Feature Dataframe 
#----------------------------------
def constructFeatureDF(featureDF) : 
    years = range(2012, 2018)
#    month_in_2012 = range(12, 13)
    month_in_general = range(1, 13)
    month_in_2017 = range(1, 6)

    for y in years : 
        if y == 2012 : 
            salesFile = 'factSalesTransactions_' + str(y) + '12' + '.csv'
            df = readAsDataframe(salesFile)
            print(salesFile)
            #getNetAmount(df)
            date = str(y) + '12'
            featureDF = setFeature(date, df, featureDF)
            #featureDF = setFeature(df, featureDF, date)
        else :     
                if y == 2017 :
                    for m in month_in_2017 : 
                        if(m < 10) :
                            salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                            #readAsDataframe(salesFile)
                            print(salesFile)
                            df = readAsDataframe(salesFile)
                            date = str(y) + str(0) + str(m)
                            #featureDF = setFeature(df, featureDF, date)
                            featureDF = setFeature(date, df, featureDF)
                        else : 
                            salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                            #readAsDataframe(salesFile)
                            print(salesFile)
                            df = readAsDataframe(salesFile)
                            date = str(y) + str(m)
                            #featureDF = setFeature(df, featureDF, date)
                            featureDF = setFeature(date, df, featureDF)
                else :
                    for m in month_in_general : 
                        if(m < 10) : 
                            salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                            #readAsDataframe(salesFile)
                            print(salesFile)
                            df = readAsDataframe(salesFile)
                            date = str(y) + str(0) + str(m)
                            #featureDF = setFeature(df, featureDF, date)
                            featureDF = setFeature(date, df, featureDF)
                        else : 
                            salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                            #readAsDataframe(salesFile)
                            print(salesFile)
                            df = readAsDataframe(salesFile)
                            date = str(y) + str(m)
                            #featureDF = setFeature(df, featureDF, date)
                            featureDF = setFeature(date, df, featureDF)
    return featureDF




"""
def readRowInDataframe(df):
    winterSeason = ['10 - Wintersport','60 - Fitness', '40 - Multisport','30 - Lifestyle']
    summerSeason = ['20 - Outdoor', '25 - Wassersport', '50 - Running', '30 - Lifestyle']

    for index, row in df.iterrows():
        season = getSeasonByMonth(row)
        getJoinedWithProduct(df)           
    
    
readRowInDataframe(joined)
"""

#-----------------------------------------------------------------------------
# For the purpose of creating training data, assign the abnormality as below
#-----------------------------------------------------------------------------
def assignNormalityValue(date, mostfreGrp):
    isNormal = False 
    winterSeason = ['10 - Wintersport','60 - Fitness', '40 - Multisport','30 - Lifestyle']
    summerSeason = ['20 - Outdoor', '25 - Wassersport', '50 - Running', '60 - Fitness', '30 - Lifestyle']

    season = getSeasonByMonth(date)
    if season == 'winter': 
        #freqSportCategory = row[' Most Frequent Product Category']
        #print freqSportCategory
        if mostfreGrp in winterSeason: 
            isNormal = True 
    else: 
        if season == 'summer':
            #freqSportCategory = row[' Most Frequent Product Category']
            #print freqSportCategory
            if mostfreGrp in summerSeason: 
                isNormal = True 
        else : 
            return 'NA'
    if isNormal == True: 
        return 'Normal'
    else:
        return 'Abnormal' 
        
    
#-------------------------------------------
# Test construct the dataframe with data 

# 1.         
#----------------------------------------------------------------------------------------------------------------------------
# Construct dataframe with 'Date', 'Most frequent Product category', 'Least frequent Product category', 'Abnormality Class'
#----------------------------------------------------------------------------------------------------------------------------
columnNames = ['Date', 'Most Frequent Product Category', 'Least Frequent Product Category', 'Abnormality Class']
index = np.arange(0)
featureDF = pd.DataFrame(columns=columnNames, index = index)

featureDF = constructFeatureDF(featureDF)
    
print(featureDF)    
featureDF.tail(5)    
    
   

# ToDo : Assign proper value in 'Abnormality class' 
# ToDo : Question : Whihch product is sold most frequently and least frequently