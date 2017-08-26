#!/usr/bin/python3
import file_reader as reader
import numpy as np
import render
from sys import argv

LIST = []
global file_name
global query_year
query_year = 2015

def checkNull(df, col):
    print("Null values detected!!")
    nanlist = df.isnull()[col].nonzero()[0].tolist()
    for i in nanlist:
        print(df[i:i+1])
        print('Total number of null values: ',len(nanlist))

def getAnnualSeasonLengths(df, col, year):
    yr = df.index.year
    y = ((yr>=year)&(yr<year+1))
    daily_mean = df[y][col].resample('D').mean()
    day_count = daily_mean.count()

    spring_and_autumn = daily_mean.map(lambda x: x < 22 and x >= 10)
    summer = daily_mean.map(lambda x: x >= 22)
    winter = daily_mean.map(lambda x: x < 10)

    print('Number of days in Summer: ',daily_mean[summer].count())
    print('Number of days in winter: ',daily_mean[winter].count())
    print('Number of days in Spinrg and Autumn: ',daily_mean[spring_and_autumn].count())

def getEvenFourSeasonTemperatureRange(df, col, year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    daily_mean = df[y][col].resample('D').mean().sort_values(axis=0)
    records_count = daily_mean.count()
    winter = daily_mean.iloc[:int(records_count/4 * 1)]
    summer = daily_mean.iloc[int(records_count/4 * 3):]
    spring_and_autumn = daily_mean.iloc[int(records_count/4):int(records_count/4 * 3)]
    #print(spring_and_autumn)
    print(summer)

def getDailySampleIntervals(df,col,year):
    day_count = 365
    if year % 4 == 0:
        day_count = 366
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    num_of_records = df[y][col].count()
    interval = num_of_records/day_count
    print('The records for year', year, 'are collected ', int(interval+0.5), 'times a day')

def getAnnualStats(df,col,year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    daily_high = df[y][col].resample('D').max()
    daily_low = df[y][col].resample('D').min()

    max = daily_high.sum()
    min = daily_low.sum()
    min = df[y][col].resample('D').min().sum()
    mean = df[y][col].resample('D').mean().sum()
    count = df[y][col].resample('D').mean().count()

    pleasant_range = df[y][col].map(lambda x: x >= 15 and x <= 25)
    pleasant_rate = len(df[y][pleasant_range])/len(df[y].index)
    acceptable_range = df[y][col].map(lambda x: x >= 10 and x < 30)
    acceptable_rate = len(df[y][acceptable_range])/len(df[y].index)

    hot_days_above_35 = daily_high.map(lambda x: x >= 35)
    hot_days_above_30 = daily_high.map(lambda x: x >= 30)
    hot_nights_above_25 = daily_low.map(lambda x: x >= 25)
    cold_days_below_10 = daily_high.map(lambda x: x < 10)
    cold_nights_below_0 = daily_low.map(lambda x: x < 0)

    print('Number of dialy records for year',year,'is ',count)
    print('Number of hot days(>=35):',daily_high[hot_days_above_35].count())
    #print(daily_high[hot_days_above_35])
    print('Number of hot days(>=30):',daily_high[hot_days_above_30].count())
    print('Number of hot nights(>=25):',daily_high[hot_nights_above_25].count())
    #print(daily_low[hot_nights_above_25])
    print('Number of cold days(<10):',daily_high[cold_days_below_10].count())
    #print(daily_high[cold_days_below_10])
    print('Number of cold nights(<0):',daily_low[cold_nights_below_0].count())
    #print(daily_low[cold_nights_below_0])

    print('The average high temperature of each day in year',year,'is: ',max/count)
    print('The average low temperature of each day in year',year,'is: ',min/count)
    print('The mean temperature of each day in year',year,'is: ', mean/count)
    print('The average value of all records of year',year,'is:',df[y][col].mean())
    print('The overall rate of',col,'between 15','and 25','of year',year,'is:',"{:.3%}".format(pleasant_rate))
    print('The overall rate of',col,'between 10','and 30','of year',year,'is:',"{:.3%}".format(acceptable_rate))

def getPeakHours(df,col):
    print('Calculating statistics for column: '+col)
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

def getAnnualTempRangeRate(df,col,year, low, high):
    num_of_records = 365*24*2
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    print('The average value of all records of year',year,'is:',df[y][col].sum()/num_of_records)
    criterion = df[y][col].map(lambda x: x >= low and x <= high)
    rate = len(df[y][criterion])/len(df[y].index)
    print('The annual rate of',col,'between',low,'and',high,'of year',year,'is:',"{:.3%}".format(rate))

def getHumidityStat(df,year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    hdf = df[y]['RHx']
    records = hdf.count()
    ex_dry = hdf.map(lambda x: x <= 15.0)
    dry = hdf.map(lambda x: x< 40.0)
    moderate = hdf.map(lambda x: x >= 40.0 and x <= 60.0)
    wet = hdf.map(lambda x: x > 60.0)
    ex_wet = hdf.map(lambda x: x > 85.0)
    print('extra dry Level Rate:',"{:.3%}".format(hdf[ex_dry].count()/records))
    print('dry Level Rate:',"{:.3%}".format(hdf[dry].count()/records))
    print('moderate Level Rate:',"{:.3%}".format(hdf[moderate].count()/records))
    print('wet Level Rate:',"{:.3%}".format(hdf[wet].count()/records))
    print('extra wet Level Rate:',"{:.3%}".format(hdf[ex_wet].count()/records))

def calculateNetEffectiveTemperature(t:float,h:float,v:float):
    return 37-(37-t)/(0.68-0.0014*h+1/(1.76+1.4*v**0.75))-0.29*t*(1-0.01*h)

def getNETStats(df,year):
     yr = df.index.year
     y = ((yr>=year)&(yr<(year+1)))
     threshold = df[y]['Temp'].map(lambda x: x <= 15.0 or x >= 26.667)
     records_count = df[y]['Temp'].count()
     app_temp_df = df[y][threshold].apply(lambda x: calculateNetEffectiveTemperature(t=x['Temp'],h=x['RHx'],v=x['Spd']), axis=1)
     print('Taking',app_temp_df.count(),'out of',records_count,'into account for Calculating NET')
     Sweat = app_temp_df.map(lambda x: x >= 27)
     Furnace = app_temp_df.map(lambda x: x >= 35)
     Chill = app_temp_df.map(lambda x: x <= 10)
     Ice = app_temp_df.map(lambda x: x <= 0)
     ChillRate=app_temp_df[threshold][Chill].count()/records_count
     IceRate=app_temp_df[threshold][Ice].count()/records_count
     SweatRate=app_temp_df[threshold][Sweat].count()/records_count
     FurnaceRate=app_temp_df[threshold][Furnace].count()/records_count
     print('Sweat Level Rate:',"{:.3%}".format(SweatRate))
     print('Furnace Level Rate:',"{:.3%}".format(FurnaceRate))
     print('Chill Level Rate:',"{:.3%}".format(ChillRate))
     print('Ice Level Rate:',"{:.3%}".format(IceRate))

def calculateHeatIndex(tempC:float,rhx:float):

    c1=16.923
    c2=0.185212
    c3=5.37941
    c4=-0.100254
    c5=9.41695*10**-3
    c6=7.28898*10**-3
    c7=3.45372*10**-4
    c8=-8.14971*10**-4
    c9=1.02102*10**-5
    c10=-3.8646*10**-5
    c11=2.91583*10**-5
    c12=1.42721*10**-6
    c13=1.97483*10**-7
    c14=-2.18429*10**-8
    c15=8.43296*10**-10
    c16=-4.81975*10**-11

    temp=tempC*1.8+32
    apparent_tempF=c1+c2*temp+c3*rhx+c4*temp*rhx+c5*temp**2+c6*rhx**2+c7*temp**2*rhx+c8*temp*rhx**2+c9*rhx**2*temp**2+c10*temp**3+c11*rhx**3+c12*temp**3*rhx+c13*temp*rhx**3+c14*temp**3*rhx**2+c15*temp**2*rhx**3+c16*temp**3*rhx**3
    apparent_tempC=(apparent_tempF-32)/1.8
    return apparent_tempC


def getHeatIndexStats(df,year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    threshold = df[y]['Temp'].map(lambda x: x >= 26.0)
    app_temp_df = df[y][threshold].apply(lambda x: calculateHeatIndex(tempC=x['Temp'],rhx=x['RHx']), axis=1)
    records_count = df[y]['Temp'].count()
    print('Taking',app_temp_df.count(),'out of',records_count,'into account for Calculating Heat Index')

    #Fatigue possible with prolonged exposure or physical activity
    Caution = app_temp_df.map(lambda x: x >= 26.6667)
    #Heat stroke, heat cramps, or heat exhaustion possible with prolonged exposure or physical activity
    ExtremeCaution = app_temp_df.map(lambda x: x >= 32.2222)
    #Heat cramps, or heat exhaustion likely, and heat stroke possible with prolonged exposure or physical activity
    Danger = app_temp_df.map(lambda x: x >= 39.4444)
    #Heat stroke highly likely
    ExtremeDanger = app_temp_df.map(lambda x: x >= 51.1111)

    CautionRate = app_temp_df[threshold][Caution].count()/records_count
    ExtremeCautionRate = app_temp_df[threshold][ExtremeCaution].count()/records_count
    DangerRate = app_temp_df[threshold][Danger].count()/records_count
    ExtremeDangerRate = app_temp_df[threshold][ExtremeDanger].count()/records_count
    print('Heat Index Caution Level Rate:',"{:.3%}".format(CautionRate))
    print('Heat Index ExtremeCaution Level Rate:',"{:.3%}".format(ExtremeCautionRate))
    print('Heat Index Danger Level Rate:',"{:.3%}".format(DangerRate))
    print('Heat Index ExtremeDanger Level Rate:',"{:.3%}".format(ExtremeDangerRate))
    print(app_temp_df[threshold][ExtremeDanger])

def getTemperatureDistribution(df,year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))
    tdf = df[y]['Temp']
    total_count = tdf.count()
    #tdf = tdf[~pd.isnull(tdf)]
    temp_dict = {key: 0 for key in range(-50, 51)}
    for t in tdf:
        if(t>0):
            t += 0.5
        else:
            t -= 0.5
        t = t.astype(int)
        if(t in temp_dict):
            temp_dict[t] += 1
    print(temp_dict)
    for key in temp_dict:
        temp_dict[key] = temp_dict[key]/total_count * 365
    render.generateBarChart(temp_dict,file_name,query_year)

if argv and len(argv)>1:

    file_name = argv[1]
    if len(argv)==3:
        query_year=int(argv[2])  
    elif len(argv)==4:
        query_year = argv[2]  
        time_zone = argv[3]

    df = reader.load2DF(file_name,query_year)

    #print(df.groupby(pd.TimeGrouper(freq='M'))['Temp'].max())

    #getPeakHours(df,'Temp')
    #checkNull(df,'Temp')

    #getAnnualStats(df,'Temp',query_year)
    #getDailySampleIntervals(df,'Temp',query_year)
    #getAnnualSeasonLengths(df,'Temp',query_year)
    #getEvenFourSeasonTemperatureRange(df,'Temp',query_year)
    #getHeatIndexStats(df,query_year)
    #getNETStats(df,query_year)
    #getHumidityStat(df,query_year)
    getTemperatureDistribution(df,query_year)

