#!/usr/bin/python3
import file_reader as reader
from sys import argv

LIST = []

def checkNull(df, col):
    print("Null values detected!!")
    nanlist = df.isnull()[col].nonzero()[0].tolist()
    for i in nanlist:
        print(df[i:i+1])
        print('Total number of null values: ',len(nanlist))

def getHumidityDistribution(df, col, year):
    yr = df.index.year
    y = ((yr>=year)&(yr<(year+1)))

    humidity_count = df[y][col].count()
    range = df[y][col].map(lambda x: x < 70 and x >= 30)
    medium_humidity_percentage = df[y][col][range].count()/humidity_count
    print('Moderate humidity percentage of year ',year,'is ',medium_humidity_percentage)

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
    hot_nights_above_25 = daily_low.map(lambda x: x >= 25)
    cold_days_below_10 = daily_high.map(lambda x: x < 10)
    cold_nights_below_0 = daily_low.map(lambda x: x < 0)

    print('Number of dialy records for year',year,'is ',count)
    print('Number of hot days(>=35):',daily_high[hot_days_above_35].count())
    print(daily_high[hot_days_above_35])
    print('Number of hot nights(>=25):',daily_high[hot_nights_above_25].count())
    print(daily_low[hot_nights_above_25])
    print('Number of cold days(<10):',daily_high[cold_days_below_10].count())
    print(daily_high[cold_days_below_10])
    print('Number of cold nights(<0):',daily_low[cold_nights_below_0].count())
    print(daily_low[cold_nights_below_0])

    print('The average high temperature of each day in year',year,'is: ',max/count)
    print('The average low temperature of each day in year',year,'is: ',min/count)
    print('The mean temperature of each day in year',year,'is: ', mean/count)
    print('The average value of all records of year',year,'is:',df[y][col].mean())
    print('The overall rate of',col,'between 15','and 25','of year',year,'is:',"{:.3%}".format(pleasant_rate))
    print('The overall rate of',col,'between 10','and 30','of year',year,'is:',"{:.3%}".format(acceptable_rate))

def getDailyPeaks(df,col):
    print(df[col].resample('D').max(),df[col].resample('D').min())

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



if argv and len(argv)>1:
    file_name = argv[1]
    if len(argv)==3:
        query_year=int(argv[2])  
    elif len(argv)==4:
        query_year = argv[2]  
        time_zone = argv[3]

    df = reader.load2DF(file_name,query_year)
    #print (df.where(df['Temp']!=np.nan))
    #print(df[df['Temp']>35])
    #getMean(df,'Temp')
    #print(df.groupby(pd.TimeGrouper(freq='M')).mean())
    #print(df.groupby(pd.TimeGrouper(freq='D'))['Temp'].max())
    getPeakHours(df,'Temp')
    #getDailyPeaks(df,'Temp')
    #checkNull(df,'Temp')
    getAnnualStats(df,'Temp',query_year)
    getDailySampleIntervals(df,'Temp',query_year)
    getAnnualSeasonLengths(df,'Temp',query_year)
