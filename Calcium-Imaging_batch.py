#!/usr/local/bin/python
'''
author:    Csaba Veraszto
date:       06/06/16
content:  Ca-imaging script, calculates dF/F. Can run in batch mode. Before running it, one has to set where your files (txt) are, you have to choose the amount of frames the script will average and calculate the minimum from to get Fo. It calculates time from the filenames. This version of the script can be run on our olt server. It has a fixed plt.ylim (y axis), which you might want to adjust, if the graph goes outside its range, but it allows you to produce equally sized images for your figures. 
				
'''



aver_range = 5 #Change: average over #frames around each value
min_range = 10 #Change:  seek out the minimum value from the #frames before the current one
mypath = ("/where/your/files/are/")  #Where your files are
  
import numpy as np
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend. Important if you run it on olt without needing an X-server.
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] #Grab all files from folder
convertedfiles = [x.encode('UTF8') for x in [f for f in listdir(mypath) if isfile(join(mypath, f))]] #Convert all filenames to UTF-8 to be safe
convertedfiles2 = [s for s in convertedfiles if ('.txt') in s] #Remove non-text files from the list.
cafiles = [s for s in convertedfiles2 if ('dt_') in s] #Remove files that does not contain dt_.
#cafiles = [s for s in convertedfiles if ('fps_') in s] #For some old fiji macros, this is what you need. See to timerate line too. 
osxbug = [s for s in cafiles if s[0:2]=="._" in s]
cafiles = [filename for filename in cafiles if filename not in osxbug]
cafiles = [s for s in cafiles if "Normalized_Neuron." not in s] #Avoid running the script on normalized data.

#Shifting average function (if aver_range = 5 then 3 values are mising from the front and 1 from the back)
def boxcar_filter(raw, box_size=aver_range):
    '''Perform boxcar filtering.'''
    import numpy as np
    box = np.ones(box_size, float) / box_size
    aboxed = np.convolve(raw, box, mode='valid')
    return aboxed


#Function to find the minimum std.deviation of a min_range window in the averaged data
def rolling_window(aboxed, min_range):
    shape = aboxed.shape[:-1] + (aboxed.shape[-1] - min_range + 1, min_range)
    strides = aboxed.strides + (aboxed.strides[-1],)
    return np.lib.stride_tricks.as_strided(aboxed, shape=shape, strides=strides)    

#Batch process list of files
for source_filename in cafiles:
	#source_filename = cafiles[0]
	neuron_in_question = "Neuron"  #If you are analysing one neuron, you can give all files the same name
	output_filename = source_filename[:-4] + "_Normalized_" + neuron_in_question + ".txt"
	output_imagename = source_filename[:-4] + "_Normalized_" + neuron_in_question + ".png"
	timerate = float(source_filename.encode('UTF8','replace')[(source_filename.encode('UTF8','replace').find('dt_')+3):(source_filename.encode('UTF8','replace').find('dt_')+7)]) 
	#timerate = float(source_filename.encode('UTF8','replace')[(source_filename.encode('UTF8','replace').find('fps_')+4):(source_filename.encode('UTF8','replace').find('fps_')+8)])                    
	title = neuron_in_question + ' activity with ' + str(round(1/timerate, 2)) + ' fps'
	from os import chdir
	chdir(mypath)
	raw = np.genfromtxt(source_filename , usecols=[1], skip_header=1)
	#Shifting average
	aboxed = boxcar_filter(raw, box_size=aver_range)
	#Find minimum in the averaged data
	F01 = min(aboxed)    
	#Find the F value with minimum std.deviation
	F02 = aboxed[np.std(rolling_window(aboxed, min_range), 1).argmin()+min_range/2]
	#dF/F calculation
	dF_F = (aboxed-F02)/F02
	np.savetxt(output_filename, dF_F, fmt=str('%.4f'), delimiter=', ', newline='\n', header='', footer='')
	#Plotting 
	y_range_low= min(dF_F)-0.9 #Change y range of the plot (can not be smaller than ply.ylim())
	y_range_high= 1.1*max(dF_F) #Change y range of the plot (can not be bigger than ply.ylim())
	import matplotlib.pyplot as plt
	plt.ioff()
	fig, ax = plt.subplots()
	#plt.ylim([y_range_low,y_range_high]) #set y axis range
	plt.ylim([-1.1,11])
	plot_range=dF_F.shape[0]
	plt.xlim([0,plot_range]) #set x axis range
	#plt.xlim([0,plot_range])
	#ax.set_aspect(plot_range/(y_range_high-y_range_low))  #uncomment this if you doesn't want to resizeable image
	#Plotted data comes next
	ax.plot(np.arange(len(dF_F)), dF_F, linewidth=2, color='black', label='''neuron_in_question''') #label='normalized original'
	fig.suptitle(title)
	#ax.legend(loc=8) 
	#import matplotlib.pyplot as plt  
	#ax.legend(loc='best') # chooses an optimal position for the legend such that it does not block lines/bars of the plot
	#remove ticks and axes
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.set_xticks([])
	ax.set_yticks([])
	font = {'family' : 'Bitstream Vera Sans',
	        'color'  : 'black',
	        'weight' : 'normal',
	        'size'   : 12,
	        }
	# draw vertical line from (70,100) to (70, 250)
	ax.arrow(0, y_range_low, 60/timerate, 0, head_width=0, head_length=0, fc='k', ec='k', lw=1.5)
	plt.text(30, y_range_low+0.02, '60 s', fontdict=font)
	ax.arrow(0, y_range_low, 0, 0.5, head_width=0, head_length=0, fc='k', ec='k', lw=1.5)
	plt.text(0.3, y_range_low+0.25, '0.5\n'r'$\Delta$F/F', fontdict=font)
	plt.savefig(output_imagename, format='png', dpi=300, bbox_inches='tight', pad_inches=0, frameon=None, transparent=True)
	plt.clf()
	#plt.ion()
	#plt.show()

	
