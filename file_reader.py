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
time_zone_prefix = 'Etc/GMT'
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


def getStationTimezone(sid):
    df0 = pd.read_csv('./stationlist.csv',header='infer',sep=',',index_col=False,dtype={'USAF':object})
    df=df0.set_index('USAF')
    tzvalue = int(df[df.index==sid].iloc[0]['TIMEZONE'])
    parsed_tzvalue = formatTimezone(tzvalue)
    print("Timezone is found for", sid, "Timezone is:", time_zone_prefix + str(tzvalue))
    return parsed_tzvalue

def getStationName(sid):
    df0 = pd.read_csv('./stationlist.csv',header='infer',sep=',',index_col=False,dtype={'USAF':object})
    df=df0.set_index('USAF')
    stn_cn_name = str(df[df.index==sid].iloc[0]['ALIAS(CH)'])
    stn_eng_name = str(df[df.index==sid].iloc[0]['ALIAS(ENG)'])
    print("Station name is", stn_cn_name, stn_eng_name)
    return stn_cn_name, stn_eng_name

def formatTimezone(tzvalue):
    parsed_tzvalue = time_zone_prefix
    if tzvalue > 0:
        parsed_tzvalue = parsed_tzvalue + str(0 - tzvalue)
    elif tzvalue < 0:
        parsed_tzvalue = parsed_tzvalue + '+' + str(0 - tzvalue)
    print('Timezone is formatted to:', parsed_tzvalue)
    return parsed_tzvalue

def get_positions(file, time_period, time_buffer):
    date_parser=lambda x: datetime.datetime.strptime(x,'%Y%m')
    df = pd.read_csv(file, sep=' ', header='infer', index_col=0, parse_dates=['DateTime'],date_parser=date_parser)
    max_row_count = df['End'].max()
    start_pos = 0
    if time_buffer == True:
        start_pos = df[df.index==df.index[df.index.year==(time_period-1)].max()].iloc[0]['Start']
    else:
        start_pos = df[df.index==df.index[df.index.year==time_period].min()].iloc[0]['Start']
    end_pos = df[df.index==df.index[df.index.year==time_period].max()].iloc[0]['End']
    return (int(start_pos), int(end_pos), int(max_row_count))

def load2DF(fname,time_period,time_buffer):
    row_range = get_positions(station_info+'/'+fname+'.info',time_period,time_buffer)
    #skipped_range = list(range(1,int(row_range[0])))+list(range(int(row_range[1])+1,int(row_range[2])+2))
    line_buffer = 10
    skipped_range = list(range(1,row_range[0]-line_buffer))
    nrows = row_range[1]-row_range[0]+line_buffer*2
    time_zone = getStationTimezone(fname)
    dateparse = lambda x: pytz.timezone('UTC').localize(datetime.datetime.strptime(x,'%Y%m%d %H%M')).astimezone(pytz.timezone(time_zone))
    df = pd.read_csv(repo_dir+'/'+fname+'.zip', compression='zip',header='infer', sep=',', encoding='us-ascii', index_col=1,parse_dates=['DateTime'],date_parser=dateparse, keep_date_col=True,dtype=datatype,keep_default_na=True,na_values=na_value_dict,skiprows=skipped_range,nrows=nrows)
    print("Climate Data of", fname, "for", time_period, "is created!")
    return df
