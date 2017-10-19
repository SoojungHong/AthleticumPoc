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


#--------------------------------------------
# function : Sum all net amount (per month)
#--------------------------------------------
def getNetAmount(df):
    
    df = df.dropna(subset=['NetAmount']) #if value is NaN, drop it 
    df = df.convert_objects(convert_numeric=True) #convert to numeric values

    netAmount = df['NetAmount'].sum()
    print(netAmount)
    return netAmount


#-----------------------------------------------------
# function : set Net amount (per month) of given 
#-----------------------------------------------------
def setSumNetAmount(df, featureDF, date):    
    df = df.dropna(subset=['NetAmount']) #if value is NaN, drop it 
    df = df.convert_objects(convert_numeric=True) #convert to numeric values
    netAmount = df['NetAmount'].sum()
    featureDF = featureDF.append({'Date': convertDate(date), 'NetAmount': netAmount}, ignore_index=True)
    #print(featureDF)
    return featureDF
 

#-----------------------------------------------------
# function : set Net amount (per month) of given 
#-----------------------------------------------------
def setFeature(df, featureDF, date):    
    df = df.dropna(subset=['NetAmount']) #if value is NaN, drop it 
    df = df.convert_objects(convert_numeric=True) #convert to numeric values
    netAmount = df['NetAmount'].sum()
    featureDF = featureDF.append({'Date': convertDate(date), 'NetAmount': netAmount, 'Weather': randint(1, 10), 'NumVisitor': randint(100, 300)}, ignore_index=True)
    return featureDF
     


#-------------------------------------------
# function : convert string to date format
#-------------------------------------------
def convertDate(dateStr): 
    date = dt.datetime.strptime(dateStr, '%Y%m')
    return date


#-----------------------------
# Test : Read one sales file
#-----------------------------
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
sales = readAsDataframe(salesFile) 
sales.info()
getNetAmount(sales)


                
#-------------------------------------------------------------------------
# Construct dataframe with 'Time', 'NetAmount', 'Weather', 'NumVisitor'
#-------------------------------------------------------------------------
columnNames = ['Date', 'NetAmount', 'Weather', 'NumVisitor']
index = np.arange(0)
featureDF = pd.DataFrame(columns=columnNames, index = index)



#-----------------------------------------
# Read all sales files (201212 - 201705)
#-----------------------------------------
years = range(2012, 2018)
month_in_2012 = range(12, 13)
month_in_general = range(1, 13)
month_in_2017 = range(1, 6)


for y in years : 
    if y == 2012 : 
        salesFile = 'factSalesTransactions_' + str(y) + '12' + '.csv'
        df = readAsDataframe(salesFile)
        print(salesFile)
        #getNetAmount(df)
        date = str(y) + '12'
        featureDF = setFeature(df, featureDF, date)
    else :     
        if y == 2017 :
            for m in month_in_2017 : 
                if(m < 10) :
                    salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                    #readAsDataframe(salesFile)
                    print(salesFile)
                    df = readAsDataframe(salesFile)
                    date = str(y) + str(0) + str(m)
                    featureDF = setFeature(df, featureDF, date)
                else : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                    #readAsDataframe(salesFile)
                    print(salesFile)
                    df = readAsDataframe(salesFile)
                    date = str(y) + str(m)
                    featureDF = setFeature(df, featureDF, date)
        else :
            for m in month_in_general : 
                if(m < 10) : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(0) + str(m) + '.csv'
                    #readAsDataframe(salesFile)
                    print(salesFile)
                    df = readAsDataframe(salesFile)
                    date = str(y) + str(0) + str(m)
                    featureDF = setFeature(df, featureDF, date)
                else : 
                    salesFile = 'factSalesTransactions_' + str(y) + str(m) + '.csv'
                    #readAsDataframe(salesFile)
                    print(salesFile)
                    df = readAsDataframe(salesFile)
                    date = str(y) + str(m)
                    featureDF = setFeature(df, featureDF, date)


print(featureDF)
featureDF.info()
featureDF

#--------------------------
# Visualize the NetAmount 
#--------------------------

# plot all attributes with its distribution
featureDF.hist(bins=50, figsize=(20,15))
plt.show()


#featureDF = featureDF.astype(np.float)
featureDF.plot.bar(figsize=(20,10), fontsize=12)
plt.show()



#------------------------------
# Split training and test data 
#------------------------------
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(featureDF, test_size=0.2, random_state=42)
train_set
test_set

featureDF_without_label = housing = train_set.drop("NetAmount", axis=1)
netAmount_labels = train_set["NetAmount"].copy()
netAmount_labels
test_labels = test_set["NetAmount"].copy()
test_labels
test_prepared = test_set.drop("NetAmount", axis=1)
test_prepared


#-------------------------------------------------------------------------------------
# The simplest (!) linear regression model 
# At the moment, the weather data and number of visitor are randomly generated one
#-------------------------------------------------------------------------------------
from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(featureDF_without_label, netAmount_labels)

from sklearn.metrics import mean_squared_error
netAmount_predictions = lin_reg.predict(test_prepared)

lin_mse = mean_squared_error(test_labels, netAmount_predictions)
lin_rmse = np.sqrt(lin_mse)
lin_rmse

#--------------------------------------
# Model with Decision Tree Regressor 
#--------------------------------------
from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor()
tree_reg.fit(featureDF_without_label, netAmount_labels) 
netAmount_tree_predictions = tree_reg.predict(test_prepared)
tree_mse = mean_squared_error(test_labels, netAmount_tree_predictions)
tree_rmse = np.sqrt(tree_mse)
tree_rmse

#---------------------------
# Cross Validation 
#---------------------------
from sklearn.model_selection import cross_val_score
scores = cross_val_score(tree_reg, featureDF_without_label, netAmount_labels, scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores = np.sqrt(-scores)

