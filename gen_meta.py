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
time_zone = 'Etc/GMT-8'
file_name = ''

def load2DF(fname):
    dateparse = lambda x: pytz.timezone('UTC').localize(datetime.datetime.strptime(x,'%Y%m%d %H%M')).astimezone(pytz.timezone(time_zone))
    df = pd.read_csv(repo_dir+'/'+fname, compression='zip',header='infer', sep=',', encoding='us-ascii', usecols=[0,1],parse_dates=['DateTime'],date_parser=dateparse, keep_date_col=True,keep_default_na=True)
    print("df is created!")
    df['rownum'] = df.index
    return df.set_index('DateTime')

def get_month_info(df, file):
    month = df.index.month
    year = df.index.year
    first_year = int(df[:1].index.year)
    end_year = int(df[-1:].index.year)
    rows = []
    #pre_index=1

    for yr in range(first_year,end_year):
        for m in range(1,13):
            start_index = df['rownum'][(year==yr)&(month==m)].min()+1
            end_index = df['rownum'][(year==yr)&(month==m)].max()+1
            row = ''
            if m < 10:
                row = str(yr)+str(m).zfill(2)+' '+str(start_index)+' '+str(end_index)
            else:
                row = str(yr)+str(m)+' '+str(start_index)+' '+str(end_index)
            rows.append(row)
            #pre_index = end_index+1
    write2File(file,rows)

def write2File(file, content):
    with open(file, 'w') as out:
        out.write('DateTime Start End\n')
        for item in content:
            out.write(item+'\n')
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
        print ("Processing file:",file)
        df = load2DF(file+'.zip')
        get_month_info(df,file+'.info')
else:
    print ('Scanning station zip files specified by user: ', file_name)
    df = load2DF(file_name+'.zip')
    get_month_info(df,file_name+'.info')
