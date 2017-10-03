#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:35:20 2017

@author: soojunghong

# Athleticum Poc data analysis 
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


#---------------------------
# function : read csv file 
#---------------------------
def readCsvFile(fileName): 
 filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
 #fileName = filePath + 'factSalesTransactions_201705.csv'
 file = filePath + fileName
 with open(file, 'rb') as f: 
     reader = csv.reader(f)
     for row in reader: 
         print row   
         
         
# Test - Open file 
readCsvFile('factSalesTransactions_201705.csv') #150704 rows 


#----------------------------------------------
# function : transform csv file to dataframe
#----------------------------------------------
def readAsDataframe(fileName): 
    filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    #fileName = filePath + 'factSalesTransactions_201705.csv'
    file = filePath + fileName 
    df = pd.read_csv(file)
    return df
    #print(df.loc[1])
    
# Test - read files as dataframe   
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
salesFile2017Apr = 'factSalesTransactions_201704.csv' #263842 rows
salesFile2016Apr = 'factSalesTransactions_201604.csv' #301714
sales2017May = readAsDataframe(salesFile) 
sales2017Apr = readAsDataframe(salesFile2017Apr)
sales2016Apr = readAsDataframe(salesFile2016Apr)
print(sales2017May) 
print(sales2017Apr)
print(sales2016Apr)
sales2017May['SalespersonID'] 
sales2017May['MembershipCardID                                  '] #this works
sales2017May['MembershipCardID'] #doesn't work
sales2017May['MembershipCardID                                  '].values
b = sales2017May['MembershipCardID                                  '].str.contains('-1')
b


#--------------------------
# groupby membership card
#--------------------------
grouped = sales2017May.groupby(sales2017May['MembershipCardID                                  '].str.contains('-1'), as_index=False)
print(grouped.size())

#-----------------------------------
# check data type of column value
#-----------------------------------
is_string_dtype(sales2017May['MembershipCardID                                  '])
#>>>> True

is_numeric_dtype(sales2017May['MembershipCardID                                  '])
#>>>> True

#-----------------------------------------
# count number of membership transaction
#-----------------------------------------
member = sales2017May.loc[sales2017May['MembershipCardID                                  '] != -1]
print(type(member))

#------------------------------------------
# Trim column names - data cleaning 
#------------------------------------------
sales2017May.columns = sales2017May.columns.str.strip()
sales2017May['MembershipCardID'] 
grouped = sales2017May.groupby(sales2017May['MembershipCardID'].str.contains('-1'), as_index=False)
print(grouped.size())


#--------------------------------------------------
# Number of sales (transactions) per store
#--------------------------------------------------
# StoreID
# df.groupby('Company Name').count()
groupByStoreID = sales2017May.groupby('StoreID')
groupByStoreID.count()
print(groupByStoreID.size()) #for each stores, count the number of transaction 
storeIdcount = groupByStoreID.size()
print(storeIdcount)
y_pos = np.arange(len(storeIdcount))
plt.bar(y_pos, storeIdcount, align='center', alpha=0.5)
plt.xticks(y_pos, storeIdcount)
plt.ylabel('Store ID')
plt.title('StoreID and Number of Transactions 2017 May')


# 2017 April sales data 
groupByStoreIDApr = sales2017Apr.groupby('StoreID')
groupByStoreIDApr.count()
print(groupByStoreIDApr.size()) #for each stores the count of transaction 
storeIdcountApr = groupByStoreIDApr.size()
print(storeIdcountApr)
y_pos_apr = np.arange(len(storeIdcountApr))
plt.bar(y_pos_apr, storeIdcountApr, align='center', alpha=0.5)
plt.xticks(y_pos_apr, storeIdcountApr)
plt.ylabel('Store ID')
plt.title('StoreID and Number of Transactions in 2017 April')


# 2016 April sales data 
groupByStoreID16Apr = sales2016Apr.groupby('StoreID')
groupByStoreID16Apr.count()
print(groupByStoreID16Apr.size()) #for each stores the count of transaction 
storeIdcount16Apr = groupByStoreID16Apr.size()
print(storeIdcount16Apr)
y_pos_16apr = np.arange(len(storeIdcount16Apr))
plt.bar(y_pos_16apr, storeIdcount16Apr, align='center', alpha=0.5)
plt.xticks(y_pos_16apr, storeIdcount16Apr)
plt.ylabel('Num transaction')
plt.title('StoreID and Number of Transactions in 2016 April')

# Question : Is there any reason why storeID 4 has the highest numbers of transaction? 
# Question : Why the higher number of store has less sales (transaction)?


#ToDo : just literally transform from string value to numeric values - instead of encoding? 
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
ProductGrp_ID = sales2016Apr["ProductGroupID"]
ProductGrp_ID = encoder.fit_transform(ProductGrp_ID)
ProductGrp_ID

#-------------------------------------------------------------
# Most frequently sold products (product category) per month 
#-------------------------------------------------------------
sales2016Apr.columns = sales2016Apr.columns.str.strip()
groupByProductID = sales2016Apr.groupby('ProductID')
groupByProductID.count().sort_values(by=['Quantity'], ascending=False)

#ToD0 : Join with ProductDim table and check the name of the product, product category

#--------------------------------------------------------------
# Least frequently sold products (product category) per month 
#--------------------------------------------------------------
sales2016Apr.columns = sales2016Apr.columns.str.strip()
groupByProductID = sales2016Apr.groupby('ProductID')
groupByProductID.count().sort_values(by=['Quantity'], ascending=True)


#question : productID -1??
temp = sales2016Apr[sales2016Apr['ProductID'].str.strip()=='-1']
temp


#ToDo : what membership customers mostly buy? What non-membership mostly buy
#create dataframe of membership and non-membership 
#sales2016Apr.loc[sales2016Apr['MembershipCardID'] == '-1'] #doesn't work
sales2016Apr
sales2016Apr.columns = sales2016Apr.columns.str.strip()
sales2016Apr

sales2016Apr['MembershipCardID'] = sales2016Apr['MembershipCardID'].str.strip()
#sales2016Apr['MembershipCardID']
sales2016Apr

#------------------------------------------
# membership and non-membership dataframe
#------------------------------------------
membership = sales2016Apr.loc[sales2016Apr['MembershipCardID'] != '-1']
membership
non_membership = sales2016Apr.loc[sales2016Apr['MembershipCardID'] == '-1']
non_membership

#ToDo : trim all values 

#ToDo : Take only necessary columns and convert values to numeric values 
#membership = membership.convert_objects(convert_numeric=True) #deprecated
membership.info()

#-------------------------------------------------------------------------
# Dataframe with only StoreID, ProductID, ProductGroupID, PurchasePrice
#-------------------------------------------------------------------------
membership_part1 = membership[['StoreID', 'ProductID', 'ProductGroupID', 'PurchasePrice']]
membership_part = membership[['ProductID', 'PurchasePrice']]

membership_part

#----------------------------------
# Correlation and scatter matrix
#----------------------------------
corr_matrix = membership_part1.corr()
corr_matrix

from pandas.tools.plotting import scatter_matrix

attributes = ['StoreID', 'ProductID', 'ProductGroupID', 'PurchasePrice']
scatter_matrix(membership_part1[attributes], figsize=(12, 8))

#----------------------------------------------------
# Data cleansing - drop if value of StoreID is NaN
#----------------------------------------------------
membership_part = membership_part.dropna(subset=['ProductID'])    # option 1
membership_part

#---------------------------------------
# clustering of membership customers
#---------------------------------------
from sklearn import cluster
k_means = cluster.KMeans(n_clusters=3)
#a = k_means.fit(np.reshape(membership_part, (len(membership_part), 1)))
a = k_means.fit(membership_part)
centroids = k_means.cluster_centers_

labels = k_means.labels_

print(centroids)
print(labels)

colors = ["g.","r.","y.","b."]

for i in centroids: plt.plot( [0, len(membership_part)-1],[i,i], "k" )
for i in range(len(membership_part)):
    plt.plot(i, membership_part[i], colors[labels[i]], markersize = 10)

plt.show()



#ToDo : gender classification using product ID and purchasing time (decision tree?) 
#ToDO : all years sales trend, find out why, can be modelled using generative approach?
#ToDO : clustering on non-membership transaction & coloring in visualization
#ToDo : First set the reason and do decision tree 
#ToDo : Transform data type from string to numeric values if necessary 
#ToDo : customer with family, especially women customers  
#ToDo : Join Product and factSalesTransactions  

#-------------------------------
# list of columns in dataframe 
#-------------------------------
columnList = sales2017May.columns.tolist()
columnList

"""
dimDateFile = 'dimDate.csv'
readAsDataframe(dimDateFile) 
"""         

#-------------------------------
# Return reason dimension file
#-------------------------------   
returnReasonFile = 'dimReturnReason.csv' #150706 rows 
dimReturnReason = readAsDataframe(returnReasonFile) 
print(dimReturnReason)          
         
 