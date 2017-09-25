# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:20:43 2017

@author: a613274
"""
#------------------------------
# Import library
#------------------------------
#import csv 
import pandas as pd
#import os
#------------------------------
# Read Sales Transaction file
#------------------------------
#myDirname = os.path.normpath("C:/Users/a613274/Downloads/AthExportData/")
salesTransactionCsv = r'C:\Users\a613274\Downloads\AthExportData\factSalesTransaction.csv'

trainData = pd.read_csv(salesTransactionCsv)
trainData