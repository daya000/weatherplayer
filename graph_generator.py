#!/usr/bin/python3
import time, datetime
import pandas as pd
import numpy as np
import glob
import os,sys,getopt
import zipfile
import pytz
import file_reader as reader
from sys import argv
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

repo_dir = './stations'
info_output_dir = './info'
LIST = []
time_zone = 'Etc/GMT-8'
file_name = '574940'
query_year = 2015
unit = 'D'


font = {'weight': 'bold',
        'size': 12
       }

colors = {
    'extremely_cold':'dark navy', 
    'very_cold':'navy', 
    'freezing':'blue',
    'cold':'skyblue', 
    'cool':'khaki', 
    'mild':'gold', 
    'warm':'orange',
    'very_warm':'salmon',
    'hot':'red',
    'very_hot':'brown',
    'extremely_hot':'black'
}

def getColorByValue(value):
    if value <= -30:
        return colors['extremely_cold']
    if value <= -15:
        return colors['very_cold']
    if value <= 0:
        return colors['freezing']
    if value < 10:
        return colors['cold']
    if value < 15:
        return colors['cool']
    if value <= 22:
        return colors['mild']
    if value <= 25:
        return colors['warm']
    if value < 30:
        return colors['very_warm']
    if value < 35:
        return colors['hot']
    if value < 40:
        return colors['very_hot']
    if value >= 40:
        return colors['extremely_hot']
    else:
        print('nan value detected!')
        return 'w'

def polyFit(x,y):
    z4 = np.polyfit(x, y, 3)
    p4 = np.poly1d(z4)
    fig.tight_layout()
    xx = np.linspace(x.min(), x.max(), 100)
    dd = mdates.num2date(xx)
    #render spine line
    cx.plot(dd, p4(xx), '-g')
    #cx.plot(dates, y, '8', color='g', markersize=5, label='blub')

def drawColoredMaxMinPlots(cx):
#render colored points representing daily max and min temperature
    cx.scatter(dates, y, s=15, c=y.apply(lambda x: getColorByValue(x)),edgecolor='face', marker='8')
    cx.scatter(dates, df_max, s=3,  c=df_max.apply(lambda x: getColorByValue(x)),edgecolor='face', marker='.')
    cx.scatter(dates, df_min, s=3,  c=df_min.apply(lambda x: getColorByValue(x)),edgecolor='face', marker='.')

def drawNormalMaxMinPlots(cx):
#render points representing daily max and min temperature in two predefined colors
    cx.errorbar(dates, df_min,
             marker='.',
             markersize=6,
             color='b',
             ecolor='b',
             markerfacecolor='b',
             capsize=0,
             linestyle='')
    cx.errorbar(dates, df_max,
             marker='.',
             markersize=6,
             color='r',
             ecolor='b',
             markerfacecolor='b',
             capsize=0,
             linestyle='')



if argv and len(argv)>1:
    file_name = argv[1]
    if len(argv)==3:
        query_year=int(argv[2])  
    elif len(argv)==4:
        query_year = argv[2]  
        time_zone = argv[3]

df = reader.load2DF(file_name,query_year, False)
yr = df.index.year
year = ((yr>=query_year)&(yr<(query_year+1)))

mpl.rc('font', **font)
mpl.rcParams['figure.figsize'] = (20.0, 10.0)
mpl.rcParams['lines.markersize'] = '4'

df_max = df[year]['Temp'].resample(unit).max()
df_min = df[year]['Temp'].resample(unit).min()
df_mean = df[year]['Temp'].resample(unit).mean()

dates = df_mean.index
x = mdates.date2num(dates.to_pydatetime())
y = df_mean

fig, cx = plt.subplots()
polyFit(x, y)

drawColoredMaxMinPlots(cx)
#drawNormalMaxMinPlots(cx)


cx.grid()
cx.set_xlim([datetime.date(query_year-1, 12, 27), datetime.date(query_year+1, 1, 5)])
cx.xaxis.set_major_locator(mpl.dates.MonthLocator(bymonth=range(1, 13)))
cx.xaxis.set_major_formatter( mpl.dates.DateFormatter('%Y-%m') )
cx.set_ylim([-50,50])
cx.set_yticks(np.arange(-50,55,5))
#cx.set_xticks(pd.date_range('2015-1-1', periods=12, freq='M'))

plt.xlabel('Date')
plt.ylabel('Temperature')

station_names = reader.getStationName(file_name)
cn_name = station_names[0].strip()
en_name = station_names[1].strip()
figure_folder_name = cn_name + '(' + en_name + ')'
figure_folder_path = './graphs/' + figure_folder_name
figure_name = figure_folder_name + '_' + file_name + '_' + str(query_year)
figure_path = './graphs/' + figure_folder_name + '/' + figure_name + '.png'

if not os.path.exists(figure_folder_path):
    os.makedirs(figure_folder_path)    

plt.savefig(figure_path, dpi=200,facecolor='ghostwhite',transparent='true')


