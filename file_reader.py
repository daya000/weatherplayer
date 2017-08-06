#!/usr/bin/python3
import time, datetime
import pandas as pd
import os,sys,getopt
import zipfile
import numpy as np
import pytz
from io import BytesIO,TextIOWrapper
from sys import argv
from dateutil.tz import tzutc
from dateutil.parser import parse

repo_dir = './stations'
station_info = './info'
LIST = []
time_zone = 'Etc/GMT-8'
file_name = ''
datatype = {
    'Spd':np.float32,
    'Hgt':np.int32,
    'Visby':np.int32,
    'Dir':np.int16,
    'Temp':np.float32,
    'Dewpt':np.float32,
    'Slp':np.float32,
    'RHx':np.float32
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
    'RHx':['999']
    }

def get_positions(file, time_period):
    date_parser=lambda x: datetime.datetime.strptime(x,'%Y%m')
    df = pd.read_csv(file, sep=' ', header='infer', index_col=0, parse_dates=['DateTime'],date_parser=date_parser)
    max_row_count = df['End'].max()
    start_pos = df[df.index==df.index[df.index.year==time_period].min()].iloc[0]['Start']
    end_pos = df[df.index==df.index[df.index.year==time_period].max()].iloc[0]['End']
    return (start_pos, end_pos, max_row_count)

def getStationTimezone(sid):
    df0 = pd.read_csv('./stationlist.csv',header='infer',sep='\t',index_col=False,dtype={'USAF':object})
    df=df0.set_index('USAF')
    print(type(df[df.index==sid])) 
    tzvalue=df[df.index==sid].iloc[0]['TIMEZONE']
    print("Timezone is found for",sid,"Timezone is:")
    return tzvalue

def load2DF(fname,time_period):

    row_range = get_positions(station_info+'/'+fname+'.info',time_period)

    skipped_range = list(range(1,int(row_range[0])))+list(range(int(row_range[1])+1,int(row_range[2])+2))
    dateparse = lambda x: pytz.timezone('UTC').localize(datetime.datetime.strptime(x,'%Y%m%d %H%M')).astimezone(pytz.timezone(time_zone))
    df = pd.read_csv(repo_dir+'/'+fname+'.zip', compression='zip',header='infer', sep=',', encoding='us-ascii', index_col=1,parse_dates=['DateTime'],date_parser=dateparse, keep_date_col=True,dtype=datatype,keep_default_na=True,na_values=na_value_dict,skiprows=skipped_range)
    print("df is created")
    return df
