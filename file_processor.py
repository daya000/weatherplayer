#!/usr/bin/python3
import os,sys 
import csv
import glob
import zipfile
from io import StringIO,BytesIO,TextIOWrapper
from sys import argv 


dir = '.'
LIST = []
HEADER_COUNT = 2
extract_folder_name = 'data_repo'
headers= ['USAF', 'DateTime','Dir','Spd', 'Hgt', 'Visby', 'Temp', 'Dewpt', 'Slp','RHx']
def skip_header(csvreader):
    i=0
    while i < HEADER_COUNT:
        next(csvreader)
        i=i+1
		
def write2zipfile(file_name, buffer):
    print ('outputing file:'+file_name,'to folder: ',extract_folder_name)
    extract_folder_path = os.path.join (dir, extract_folder_name)
    if not os.path.exists(extract_folder_path):
    	print ('Creating new folder: ', extract_folder_path)
    	os.mkdir(extract_folder_path)
    string_buffer = StringIO()
    csvwriter = csv.DictWriter(string_buffer,fieldnames=headers, restval='',extrasaction='raise')
    csvwriter.writeheader()

    for row in buffer: 
        formatted = {
    		headers[0]:row[0],
    		headers[1]:row[2]+' '+row[3],
            	headers[2]:row[7],
            	headers[3]:row[10],
    		headers[4]:row[12],
    		headers[5]:row[16],
    		headers[6]:row[20],
    		headers[7]:row[22],
    		headers[8]:row[24],
            	headers[9]:row[26]
    		}
        if row[16] != '      ':
            formatted['Visby'] = row[16]
        else:
            formatted['Visby'] = '999999'
        csvwriter.writerow(formatted)
    print('First record'+str(buffer[0]))
    print('Second record'+str(buffer[1]))
    print('Thrid record'+str(buffer[2]))
    print('Last record date: '+str(buffer[-1]))
    with zipfile.ZipFile(os.path.join(extract_folder_path,file_name+'.zip'),'w') as filezip:
    	print ('Writing csv into package file:',file_name+'.zip')
    	filezip.writestr(file_name+'.csv',string_buffer.getvalue())
if argv and len(argv) > 1:
    dir=argv[1]
print ('Searching zip files in the base folder: ',dir)
for name in glob.glob(dir+'/*.zip'):
    LIST.append(os.path.splitext(os.path.basename(name))[0])
print ('The package files are found: \n',LIST)

if LIST !=[]:
	for file in LIST:
		Stations = []
		print('processing the zip file:',file)
		filehandle = open(dir+'/'+file+'.zip','rb') 
		zfile = zipfile.ZipFile(filehandle) 
		zfile_bytes = BytesIO(zfile.read(file+'.txt'))
		data = TextIOWrapper (zfile_bytes,encoding='ascii') 
		csvreader = csv.reader(data,delimiter=',')
		if HEADER_COUNT > 0:
			skip_header(csvreader)
		sid = ''
		buffer = []
		for row in csvreader:
			if sid == '':
				sid = row[0]
				buffer.append(row)
				Stations.append(sid)
			elif row[0] == sid:
				buffer.append(row)
			else:
				print ('Generating package file: ',row[0])
				write2zipfile(sid,buffer)
				buffer =[]
				sid = row[0]
				buffer.append(row)
				Stations.append(sid)
		print ('Hits the last station, write its data to buffer...') 
		write2zipfile(sid,buffer)
		print ('In the RAW package file: '+file+'.zip','these packages were created by station ID:\n'+str(Stations))
		buffer = []
