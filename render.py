import matplotlib as mpl
import numpy as np
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generateBarChart(D,file_name,query_year):

    sorted_keys = sorted(tuple(D))
    sorted_values = []
    
    counter = 0
    for i in sorted_keys:
        print(i,D[i])
        sorted_values.insert(counter,D[i])
        counter+=1

    print(sorted_keys)
    print(sorted_values)

    #len(sorted_keys)
    len(sorted_values)
    #sorted(D.items,key=lambda item:int(item[0]))
    mpl.rcParams['figure.figsize'] = (40.0, 10.0)
    plt.bar(sorted_keys, sorted_values, align='center')
    plt.xticks(sorted_keys, list(sorted_keys))

    plt.yticks(np.arange(0, 55, 5))
    
    plt.xlabel('Temperature')
    plt.ylabel('Count')
    plt.savefig('./graphs/'+file_name+'_temp_distribution_'+str(query_year)+'.png', dpi=200,facecolor='ghostwhite',transparent='true')
