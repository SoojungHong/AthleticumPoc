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
 #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
 atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
 #fileName = filePath + 'factSalesTransactions_201705.csv'
 file = atosFilePath + fileName
 with open(file, 'rb') as f: 
     reader = csv.reader(f)
     for row in reader: 
         print row   
         
         
# Test - Open file 
readCsvFile('factSalesTransactions_201705.csv') #150704 rows 
readCsvFile('dimProduct.csv')

#----------------------------------------------
# function : transform csv file to dataframe
#----------------------------------------------
def readAsDataframe(fileName): 
    #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
    #fileName = filePath + 'factSalesTransactions_201705.csv'
    file = atosFilePath + fileName 
    #df = pd.read_csv(file)
    #ToDo : if the value between comma is empty, delete the cell
    df = pd.read_csv(file, error_bad_lines=False)
    return df
    #print(df.loc[1])
    
# Test - read files as dataframe   
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
salesFile2017Apr = 'factSalesTransactions_201704.csv' #263842 rows
salesFile2016Apr = 'factSalesTransactions_201604.csv' #301714
dimProduct = 'dimProduct.csv'
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
member.count()
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
sales2016Apr.info() 
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

#ToDo : Join with ProductDim table and check the name of the product, product category

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
non_membership.info()

#ToDo : trim all values 

#------------------------------------------------
# Convert values from Object to numeric values 
#------------------------------------------------
membership = membership.convert_objects(convert_numeric=True) #deprecated
membership.info()

non_membership = non_membership.convert_objects(convert_numeric=True)
non_membership.info()

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


#-------------------------------
# list of columns in dataframe 
#-------------------------------
columnList = sales2017May.columns.tolist()
columnList
         

#-------------------------------
# Return reason dimension file
#-------------------------------   
returnReasonFile = 'dimReturnReason.csv' #150706 rows 
dimReturnReason = readAsDataframe(returnReasonFile) 
print(dimReturnReason)          
  

#------------------------------------------------------------------------------------
# ToDo : Find product - product correation with sales or with membership customer
#------------------------------------------------------------------------------------
# Product Group dimension : 253 rows 
dimProductGroupFile = 'dimProductGroup.csv' 
dimProductGroup = readAsDataframe(dimProductGroupFile)
dimProductGroup
# ToDo : there are NaN or -1 values. Maybe data cleaning is needed
# ToDo (Question) : What is Universal Code? Why some value is -1

# Product dimension 
dimProductFile = 'dimProduct.csv'
dimProduct = readAsDataframe(dimProductFile) 
dimProduct
dimProduct.head(5)
#ToDo : (File error) original data seems not clean - e.g. there are more columns than it should be?

#---------------------------------------------------------------
# Join 'Sales2016Apr's membership data' data and 'dimProduct' 
#---------------------------------------------------------------
membership = sales2016Apr.loc[sales2016Apr['MembershipCardID'] != '-1']
membership
membership.head(5)

#import pandas as pd
# inner join 
joined = pd.merge(dimProduct, membership, on='ProductID', how='inner')
joined.head(5)
joined.tail(5)

# From Joined dataframe select only 
# 'TimeID', 'ProductID', 'ProductGroupID', 'MembershipCardID', 'PurchasePrice' 
# 'ProductFamilyCodeDesc', 'ProductCodeDesc', 'GenderCodeDesc' 
joined_partial = joined[['TimeID', 'ProductID', 'ProductGroupID', 'MembershipCardID', 'PurchasePrice', 'ProductFamilyCodeDesc', 'ProductCodeDesc', 'GenderCodeDesc']]
joined_partial

joined_gender_info = joined[['TimeID', 'ProductID', 'ProductGroupID', 'MembershipCardID', 'ProductCodeDesc', 'GenderCodeDesc']]
joined_gender_info
joined_gender_info.loc[joined_gender_info['GenderCodeDesc'].str.contains('20 - Herren')]
# member = sales2017May.loc[sales2017May['MembershipCardID                                  '] != -1]

gender_grouped = joined_gender_info.groupby(joined_gender_info['GenderCodeDesc'].str.contains('Herren'), as_index=False)
print(gender_grouped.size())


#-------------------------
# Product Gender Ratio
#-------------------------
def productGenderRatio(df, dimProduct): 
    # clean column name
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['ProductID']) 

    membership = df.loc[df['MembershipCardID'] != '-1']
   
    joined = pd.merge(dimProduct, membership, on='ProductID', how='inner')
    joined_gender_info = joined[['TimeID', 'ProductID', 'ProductGroupID', 'MembershipCardID', 'ProductCodeDesc', 'GenderCodeDesc']]
    
    gender_grouped = joined_gender_info.groupby(joined_gender_info['GenderCodeDesc'].str.contains('Herren'), as_index=False)
    print(gender_grouped.size())

# product gender on sales2017Apr
salesFile2017Apr = 'factSalesTransactions_201704.csv' #263842 rows
dimProduct = 'dimProduct.csv'

sales2017Apr = readAsDataframe(salesFile2017Apr)
sales2017Apr #263842
product = readAsDataframe(dimProduct)
product #559657 - Excel shows 621544
productGenderRatio(sales2017Apr, product)

# product gender on sales2017May
salesFile2017May = 'factSalesTransactions_201705.csv' #263842 rows
dimProduct = 'dimProduct.csv'

sales2017May = readAsDataframe(salesFile2017May)
product = readAsDataframe(dimProduct)
productGenderRatio(sales2017May, product)

# product gender on sales2017March
salesFile2017March = 'factSalesTransactions_201703.csv' #263842 rows
dimProduct = 'dimProduct.csv'

sales2017March = readAsDataframe(salesFile2017March)
product = readAsDataframe(dimProduct)
productGenderRatio(sales2017March, product)
"""
GenderCodeDesc
False     67984
True     112824
"""


#------------------------------------------------------------------------
# From dimProduct file, calculate the ratio of gender indicated product 
#------------------------------------------------------------------------
dimProduct = 'dimProduct.csv'
product = readAsDataframe(dimProduct)
product.head(5)
# 'GenderCodeDesc', 'SaisonCode'
# groupby and count
product.info()
product.groupby(['GenderCodeDesc']).size() 
product.groupby(['SaisonCodeDesc']).size() 
product.groupby(['GenderCodeDesc', 'SaisonCode']).size().reset_index(name='counts')
product.groupby(['SaisonCode']).size().reset_index(name='counts')



# Question : is it always sale of male product is twice bigger than female product?
# Answer : Because there are more male related product. In average, two times more male products than female products

#----------------------------------------------------------------
# Analyze product gender description on Non-membership customer 
#----------------------------------------------------------------
def productGenderRatioNonMember(df, dimProduct): 
    # clean column name
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['ProductID']) #251550
    # non-membership customers 
    non_membership = df[df['MembershipCardID'].str.contains('-1')] 
    print(non_membership.info())
    print(dimProduct.info())
    
    # Before join (merge), you have to convert data type to numeric, otherwise merge wouldn't work!
    non_membership =  non_membership.convert_objects(convert_numeric=True)
    dimProduct = dimProduct.convert_objects(convert_numeric=True)
    
    # inner join 'non_membership' and 'dimProduct' dataframe
    joined = pd.merge(dimProduct, non_membership, on='ProductID', how='inner')
    # show gender code description of 
    print(joined.groupby(['GenderCodeDesc']).size())



#----------------------------------------------------------------
# Analyze product gender description on Non-membership customer 
#----------------------------------------------------------------
def productGenderRatioMembership(df, dimProduct): 
    # clean column name
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['ProductID']) #251550
    # non-membership customers 
    membership = df[df['MembershipCardID'].str.contains('-1') == False] 
    print(membership.info())
    print(dimProduct.info())
    
    # Before join (merge), you have to convert data type to numeric, otherwise merge wouldn't work!
    membership =  membership.convert_objects(convert_numeric=True)
    dimProduct = dimProduct.convert_objects(convert_numeric=True)
    
    # inner join 'non_membership' and 'dimProduct' dataframe
    joined = pd.merge(dimProduct, membership, on='ProductID', how='inner')
    # show gender code description of 
    print(joined.groupby(['GenderCodeDesc']).size())

   
#------------------------------
# Get membership customer
#------------------------------
def getMembershipCustomer(df): 
    # clean column name
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['ProductID']) #251550
    membership = df[df['MembershipCardID'].str.contains('-1') == False] #23898
    print(membership)


#--------------------------------------------------------------------------
# product gender analysis on sales2017March for Non-membership customers
#--------------------------------------------------------------------------
salesFile2017March = 'factSalesTransactions_201703.csv' #263842 rows
dimProduct = 'dimProduct.csv'

sales2017March = readAsDataframe(salesFile2017March)
product = readAsDataframe(dimProduct) #ToDo : unclean data

productGenderRatioNonMember(sales2017March, product)

"""
Question : Why 'GenderCodeDesc' has same # of classes
10 - Damen      5481
20 - Herren    10835
30 - Kinder     3264
"""
sales2017March.columns = sales2017March.columns.str.strip()
sales2017March = sales2017March.dropna(subset=['ProductID']) 
sales2017March.info()
sales2017March = sales2017March.convert_objects(convert_numeric=True)



#---------------------------------------------------------------------
# product gender analysis on sales2017March for membership customers
#---------------------------------------------------------------------
salesFile2017March = 'factSalesTransactions_201703.csv' #263842 rows
dimProduct = 'dimProduct.csv'

sales2017March = readAsDataframe(salesFile2017March)
product = readAsDataframe(dimProduct) #ToDo : unclean data
productGenderRatioMembership(sales2017March, product)


#----------------------
# product Group file  
#----------------------
productGrpFile = 'dimProductGroup.csv' 
productGrp = readAsDataframe(productGrpFile)
productGrp.head(5)
productGrp.info()

# CategoryDesc
productGrp.groupby(['CategoryDesc']).size()

# UniverseDesc
productGrp.groupby(['UniverseDesc']).size()

# ProductGroupDesc 
productGrp.groupby(['ProductGroupDesc']).size()
productGrp.groupby(['ProductGroupID']).size()

# class 
productGrp.groupby(['ClassDesc']).size()

#-----------------------------------------------------------
# Find out outlier product (e.g. winter product in summer)
#-----------------------------------------------------------
# Finding (to join)
# product group's universe code is same as product universe code 
# product group's 'ProductGroupDesc' is same as ''WarengroupCodeDesc'

dimProduct = 'dimProduct.csv'
product = readAsDataframe(dimProduct) #ToDo : unclean data
product.info()
product.head(5)
product.groupby(['UniverseCodeDesc']).size()

product.groupby(['UniverseCode']).size()

product.groupby(['ProductFamilyCodeDesc']).size()

product.groupby(['WarengroupCodeDesc']).size() # 101 - Alpinski
product.groupby(['WarengroupCode']).size() # 101 - Alpinski

#----------------------------------------
# summer sales data example (2016 Aug)
#----------------------------------------
salesFile2016Aug = 'factSalesTransactions_201608.csv' #263842 rows
sales2016Aug = readAsDataframe(salesFile2016Aug)
sales2016Aug.head(5)
sales2016Aug = sales2016Aug.convert_objects(convert_numeric=True)
sales2016Aug.columns = sales2016Aug.columns.str.strip()

product.columns = product.columns.str.strip()
product = product.dropna(subset=['ProductID']) #251550
product = product.convert_objects(convert_numeric=True)
product.info()
   
joined = pd.merge(product, sales2016Aug, on='ProductID', how='inner')
joined.info()
warenGroupBy = joined.groupby(['WarengroupCodeDesc']).size() # 101 - Alpinski
warenGroupBy

universeGroupBy = joined.groupby(['UniverseCodeDesc']).size() # 10 wintersport
universeGroupBy

"""
UniverseCodeDesc
10 - Wintersport                         452
20 - Outdoor                           50973
25 - Wassersport                       25848
30 - Lifestyle                         17094
40 - Multisport                        24778
50 - Running                           15192
60 - Fitness                           46927
70 - Ballsport                         42338
80 - Velo/Rollers                      28506
85 - Unterw�sche                       10351
90 - Services/Miete/Aussersortiment      398
99 - N/A       """


#----------------------------------------
# winter sales data example (2016 Dec)
#----------------------------------------
salesFile2016Dec = 'factSalesTransactions_201612.csv' #263842 rows
sales2016Dec = readAsDataframe(salesFile2016Dec)
sales2016Dec.head(5)
sales2016Dec = sales2016Dec.convert_objects(convert_numeric=True)
sales2016Dec.columns = sales2016Dec.columns.str.strip()

product.columns = product.columns.str.strip()
product = product.dropna(subset=['ProductID']) #251550
product = product.convert_objects(convert_numeric=True)
product.info()
   
joined = pd.merge(product, sales2016Dec, on='ProductID', how='inner')
joined.info()
warenGroupBy = joined.groupby(['WarengroupCodeDesc']).size() # 101 - Alpinski
print(type(warenGroupBy))

universeGroupBy = joined.groupby(['UniverseCodeDesc']).size() # 10 wintersport
universeGroupBy.sort_values(ascending=True) # sorting the Series with ascending order

"""
UniverseCodeDesc
10 - Wintersport                       54384
20 - Outdoor                           26059
25 - Wassersport                        6014
30 - Lifestyle                         21545
40 - Multisport                        26772
50 - Running                           14308
60 - Fitness                           33990
70 - Ballsport                         27914
80 - Velo/Rollers                      14044
85 - Unterw�sche                       30791
90 - Services/Miete/Aussersortiment     3680
99 - N/A                                   6
"""

# ToDo : Create Dataframe from groupby result  and visualize the histogram or chart 
universeGroupBy.get('10 - Wintersport')
import numpy as np
#import pandas
columns = ['Month', '10 - Wintersport', '25 - Wassersport', '50 - Running']
index = np.arange(0) # array of numbers 12 (12 month)
universeDF = pd.DataFrame(columns=columns, index = index)
universeDF
#universeDF = universeDF.set_value(len(universeDF), 'Month', 'December')
#universeDF = universeDF.set_value(len(universeDF), '10 - Wintersport', 54384)
#universeDF = universeDF.set_value(len(universeDF), '25 - Wassersport', 6014)
universeDF = universeDF.append({'Month':12, '10 - Wintersport': 54384, '25 - Wassersport' : 6014, '50 - Running':14308}, ignore_index=True)
universeDF = universeDF.append({'Month':8, '10 - Wintersport': 452, '25 - Wassersport' : 25848, '50 - Running':15192}, ignore_index=True)
universeDF

universeDF = universeDF.astype(np.float)
#universeDF.hist(column= '50 - Running')

universeDF.plot.hist()



"""
--------------------------------------------
Month ¦ Wintersport ¦ Wassersport ¦ Running 
--------------------------------------------
 Jan  ¦    123      ¦  342        ¦ 3242
--------------------------------------------
 Feb  ¦    489      ¦  898        ¦ 423 
-------------------------------------------- 

"""

# ToDo : check the trend or change of numbers in each UniverseCode Description in each month 
# for each month, and check the trend

# ToDo : Construct dataframe with features with all times and purchased product 

#ToDo : gender classification using product ID and purchasing time (decision tree?) 
#       This can't be solved directly, because there is no labels, so not a supervised learning
#ToDo : all years sales trend, find out why, can be modelled using generative approach?
#ToDo : clustering on non-membership transaction & coloring in visualization
#ToDo : First set the reason and do decision tree 
#ToDo : customer with family, especially women customers  
#ToDo : Join Product and factSalesTransactions  
#ToDo : Find correlation with date and product (group)
       
 