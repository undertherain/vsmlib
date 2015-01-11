#!/usr/bin/env python3
import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import glob

myColors = ["b", "g", "r", "c", "m", "y", "k", "b", "k", "c"]

argv = sys.argv
if len(argv) < 2:
	print ("direcrory name required")
	exit()
name_dir = argv[1]


max_x = 0
max_y = 0
legends = []
files = glob.glob(name_dir+"/*")
i = 1;
dic_df = {}

for name_file in files:
	try:
		print("parsing "+name_file)
		fileIn=open(name_file,'r')
#		dataframe=pandas.read_csv(fileIn,header=True,names=['keys','throughput'])	
		dataframe=pandas.read_csv(fileIn,header=True, sep='\t',names=['keys','throughput','xxxx'])	
		if not isinstance(dataframe.iloc[0,0], (int, float, complex)): #must be header #long for python 2.x
			dataframe.drop(0,axis=0,inplace=True)
		dataframe=dataframe.applymap(lambda x: float(x)/1000000.0)
		dic_df[name_file[len(name_dir):]]=dataframe
	except:
		print ("error parsing file", name_file)
		raise	

concatenated = pandas.concat(list(dic_df.values()), keys=dic_df.keys())
#max_x=concatenated.max()
max_x=concatenated.max()['keys']
max_y=concatenated.max()['throughput']+15

for name_file in files:
		#plt.subplot(len(files),1,i)
		i+=1
		#reshape_factor=10
		dataframe=dic_df[name_file[len(name_dir):]]
		size=len(dataframe.index)
		#new_size=size/reshape_factor*reshape_factor
		#dataframe_averaged=dataframe.groupby('keys').mean()

		p1=plt.plot(dataframe['keys'],dataframe['throughput'], myColors[0],linewidth=1,linestyle='-', marker='o',markersize=0,markeredgewidth=0)
		x=(np.float_(dataframe['keys']))
		y=(np.float_(dataframe['throughput']))
		#print (y)
		heatmap,xedges,yedges=np.histogram2d(y,x, bins=50)
		#print(heatmap[::-1])
		#im = plt.pcolor(heatmap,cmap=mpl.cm.Blues)

		dataframe_averaged = dataframe.groupby('keys').aggregate([np.mean, np.std, np.max, np.min])
		#print(dataframe_averaged['throughput'])
		#p2=plt.plot(dataframe_averaged.index,dataframe_averaged['throughput','mean'], myColors[0],linewidth=1)
		#p1=plt.plot(dataframe_averaged.index,dataframe_averaged['throughput','amax'], myColors[0],linewidth=1)
		#p1=plt.plot(dataframe_averaged.index,dataframe_averaged['throughput','amin'], myColors[0],linewidth=1)
		#p1=plt.plot(lstSizesErr,lstStdDeviation, myColors[0],linewidth=1)
		#errs=plt.errorbar(dataframe_averaged.index, dataframe_averaged['throughput','mean'], yerr=dataframe_averaged['throughput','std'], fmt='o-')

#		lstSizes=dataframe[dataframe.columns[0]].reshape(-1,reshape_factor).mean(axis=1)
#		lstPerf=dataframe[dataframe.columns[1]].reshape(-1,reshape_factor).mean(axis=1)
#		lstErr=dataframe[dataframe.columns[1]].reshape(-1,reshape_factor).std(axis=1)

		legends.append(name_file[len(name_dir):])
		myColors=myColors[1:]
		plt.ylabel('Unique words, (millions)', weight="bold")
		plt.xlabel('Total words, (millions)', weight="bold")
		#plt.ylim([0,max_y+1])
		#plt.xlim([0,max_x+1])
		#plt.xticks(np.arange(0,  max_x+1, 2.0))
		plt.grid(True)
		#plt.title(name_file[len(name_dir):])

plt.subplots_adjust(left=0.08, right=0.97, top=0.97, bottom=0.08)
#plt.savefig('temp.png', transparent=True)
plt.legend(legends,loc=8,ncol=2).draggable()
plt.savefig('unique_words.pdf',transparent=True)
plt.show()
quit()

