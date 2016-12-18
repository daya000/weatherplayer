#!/usr/bin/python3
import time, datetime
import pandas as pd
import glob
import os,sys,getopt
import zipfile
import numpy as np
import pytz
from io import BytesIO,TextIOWrapper
from sys import argv
from dateutil.tz import tzutc
from dateutil.parser import parse
repo_dir = './stations'
LIST = []
time_zone = 'Asia/Shanghai'
file_name = ''
datatype = {
    'Spd':np.float32,
    'Hgt':np.int32,
    'Visby':np.int32,
    'Dir':np.int16,
    'Temp':np.float32,
    'Dewpt':np.float32,
    'Slp':np.float32,
    'RHx':np.int8
    }
#Add na_values=na_value_dict in pd.read_csv() arguments
na_value_dict = {
    'Spd':['999.9'],
    #'Hgt':['99999'],
    #'Dir':['999'],
    #'Visby':['999999'],
    'Temp':['999.9'],
    'Dewpt':['999.9'],
    'Slp':['9999.9'],
    #'RHx':['999']
    }
def checkNull(df, col):
    print("Null values detected!!")
    nanlist = df.isnull()[col].nonzero()[0].tolist()
    for i in nanlist:
        print(df[i:i+1])
        print('Total number of null values: ',len(nanlist))
def load2DF(fname):
    #date_parser=lambda x: timezone('America/New_York').localize(datetime.datetime.strptime(x,'%Y%m%d%H:%M:%S.%f')).astimezone(timezone('CET'))
    dataparse = lambda x: pytz.timezone('UTC').localize(datetime.datetime.strptime(x,'%Y%m%d %H%M')).astimezone(pytz.timezone(time_zone))
    df = pd.read_csv(repo_dir+'/'+fname, compression='zip',header='infer', sep=',', encoding='us-ascii', index_col=1,parse_dates=['DateTime'],date_parser=dataparse, keep_date_col=True,dtype=datatype,keep_default_na=True,na_values=na_value_dict)
    print(df[:-30])
    return df
def getAnnualPeaks(df,col,year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    max = df[y][col].resample('D').max().sum()
    min = df[y][col].resample('D').min().sum()
    print('The average high Temperature of each day in year',year,'is: ',max)
    print('The average low Temperature of each day in year',year,'is: ',min)
    print('The average Temperature of each day in year',year,'is: ',(max+min)/365/2)

def getDailyPeaks(df,col):
    print(df[col].resample('D').max(),df[col].resample('D').min())

def getPeakHours(df,col):
    print('Calculating statistics for column: '+col_name)
    dic = {}
    hr = df.index.hour
    for temp in range(0,24):
         tempHigh = ((hr >= temp)&(hr < (temp+1)))
         dic[temp] = df[tempHigh][col].sum()
         print('Total sum of High temp in this hour',str(temp),': ',dic[temp])
         #print(str(col),df[tempHigh][col][:10])
def getMean(df,col_name):
    #temp = df.as_matrix(columns=[df['Temp']])
    #print (np.average(temp))
    print ('The total number of NaN values on column '+col_name+' is: ',df[col_name].isnull().sum())
    print(df[col_name].mean())
def getAnnualStat(df,col,year, low, high):
    num_of_records = 365*24*2
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    print('The average value of all records of year',year,'is:',df[y][col].sum()/num_of_records)
    criterion = df[y][col].map(lambda x: x >= low and x <= high)
    rate = len(df[y][criterion])/len(df[y].index)
    print('The annual rate of',col,'between',low,'and',high,'of year',year,'is:',"{:.3%}".format(rate))
if argv and len(argv)>1:
    file_name = argv[1]
    if len(argv)>2:
        time_zone = argv[2]
if file_name == '':
    print ('Scanning station zip files in the base folder: ', repo_dir)
    for name in glob.glob(repo_dir+'/*.zip'):
        LIST.append(os.path.splitext(os.path.basename(name))[0])
    print ('The package files are found: \n',LIST)
    for file in LIST:
        df = load2DF(file+'.zip')
else:
    print ('Scanning station zip files specified by user: ', file_name)
    df = load2DF(file_name+'.zip')
    #print (df.where(df['Temp']!=np.nan))
    #print(df[df['Temp']>35])
    #getMean(df,'Temp')
    #print(df.groupby(pd.TimeGrouper(freq='M')).mean())
    #print(df.groupby(pd.TimeGrouper(freq='D'))['Temp'].max())
    #getPeakHours(df,'Temp')
    #getDailyPeaks(df,'Temp')
    getAnnualPeaks(df,'Temp',2015)
    #checkNull(df,'Temp')
    getAnnualStat(df,'Temp',2015,15,25)
    getAnnualStat(df,'Temp',2015,10,30)
