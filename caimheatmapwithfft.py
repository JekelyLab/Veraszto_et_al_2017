#!/usr/local/bin/python
'''
author:    Csaba Veraszto MPI for Developmental Biology Tübingen AG-Jekely
date:      Jan 2017
content:      Calculating the periods of neuron activities (calcium-imaging)
Notes on FFT: We aim to show the characteristic frequencies of our 'finite functions' and we don't care about the amplitudes. Thus taking only the real part of the fft and squaring it/taking their absolute value would give us all the frequency maximas as positive peaks (the amplitudes won't be correct). 
'''

import os
from os import chdir, rename, listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
#from scipy.fftpack import fft
import matplotlib.pyplot as plt
from matplotlib import pyplot

#Find all files in subfolders
path = '/where/your/files/are/'
dst = '/destination/folder/'
Normtext = [os.path.join(root, name) for root, dirs, files in os.walk(path) for name in files if name.endswith("Normalized_Neuron.txt")] #Find all normalized calcium imaging data

#The next part can deal with hidden files in OSX
#osxbug = [s for s in Normtext if s[0:2]=="._" in s]
#for item in Normtext:
#    history1.write("%s\n" % item)

MC = [s for s in Normtext if "MCValues" in s] #Select files about one neuron

#Do you have any duplicates or identical names ?
import collections
print [item for item, count in collections.Counter(MC).items() if count > 1]

#Create a copy of every files. I can't change the names if it's not a copy, and if I can't do that, I can't extract frame information later. If I would change the name somehow, the link would not point to the original file anymore. 
from shutil import copy
for s in MC:
    copy(s, dst)

'''
#This part can deal with  filenames generated by the old script
MCunity=[]
for s in MC:
    b = s.replace('fps_', 'dt_')
    MCunity.append(b)
'''

#This part can deal with  filenames generated by the old script
chdir(dst)
fnames = listdir(dst)
for filename in os.listdir(dst):
    newname = filename.replace('_fps_', '_dt_')
    os.rename(filename, newname)

#Create DataFrame
chdir(dst)
files = [f for f in listdir(dst) if isfile(join(dst, f)) and "_Normalized_Neuron.txt" in f]
files2 = [f for f in files if "1.11" in f or "1.1088" in f]
dfcaim = pd.DataFrame() 
dt = 'dt_'
import re 
for s in files2:
   .....:     name = s
   .....:     frames = float(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", name[name.find(dt):len(name)])[0])
   .....:     data = np.loadtxt(name)
   .....:     #print data[:5]
   .....:     df1 = pd.DataFrame()
   .....:     df1 = pd.DataFrame(data[:500])
   .....:     df1 = df1.T
   .....:     dfcaim = dfcaim.append(df1)
   .....:     #print len(data), frames, s[0:30]
   .....:     print dfcaim.shape



#Calculate the periods one by one
plt.clf()
name = files2[96]
dt = 'dt_'
import re 
frames = float(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", name[name.find(dt):len(name)])[0])
data = np.loadtxt(name)
X = data
N = len(data)
W = np.fft.fft(X)
freq = np.fft.fftfreq(X.shape[-1])
yaxis = [frames*float(i) for i in np.arange(0, N)]   
pyplot.subplot(211)
pyplot.plot(yaxis, data)
pyplot.xlabel("time (sec)")   
pyplot.subplot(212)
#ax = fig.add_subplot(212)
pyplot.plot(frames/freq[1:N/2], abs(W[1:N/2]))
for x, y in zip(frames/freq[1:N/2], abs(W[1:N/2])):
    if x>10 and x<500:
	pyplot.text(x, y, str(x)[:6], fontsize=9, color='black')

pyplot.xlabel(r"$1/f$")
pyplot.show()


#CSV files for heatmap
dfdf = dfcaim
dfdf.columns = np.arange(0, 500)*frames
rows = ['''input FFT data''']
dfrows = pd.DataFrame(rows)
dfdf.to_csv('dfdf_with_columns.csv') #You have to reorder the rows. 
finaldf= pd.read_csv('dfdf_with_columns2.csv', header = 0, index_col=0) #This file is the one with ordered fft periods. 

#HEATMAP
import seaborn as sns
#f, ax = plt.subplots()
cmap = sns.palplot(sns.color_palette("coolwarm", 7))
#sns.heatmap(df_norm, cmap=cmap, xticklabels=10, yticklabels=False, linewidths=0, cbar_kws={"shrink": 1}, ax=ax)
ax = sns.heatmap(finaldf, cmap=cmap, robust=True, xticklabels=100, yticklabels=5, linewidths=False, cbar_kws={"shrink": 1}, cbar=False)
plt.ion()
plt.show()

#Create DataFrame and calculate FFTs.
dfcaim = pd.DataFrame() 
for s in files2:
   .....:     name = s
   .....:     frames = float(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", name[name.find(dt):len(name)])[0])
   .....:     data = np.loadtxt(name)
   .....:     #print data[:5]
   .....:     X = data
   .....:     N = len(data)
   .....:     W = np.fft.fft(X)
   .....:     freq = np.fft.fftfreq(X.shape[-1])   
   .....:     from scipy.signal import find_peaks_cwt
   .....:     indexes = find_peaks_cwt(abs(W), np.arange(1, 200))
   .....:     threshold = max(abs(W)[indexes])-0.00000001
   .....:     idx = np.where(abs(W)>threshold)
   .....:     yaxis = [frames*float(i) for i in np.arange(0, N)]   
   .....:     pyplot.subplot(211)
   .....:     pyplot.plot(yaxis, data)
   .....:     pyplot.xlabel("time (sec)")   
   .....:     pyplot.subplot(212)
   .....:     #ax = fig.add_subplot(212)
   .....:     pyplot.plot(frames/freq[1:N/2], abs(W[1:N/2]))
   .....:     for x, y in zip(frames/freq[1:N/2], abs(W[1:N/2])):
   .....:         if x>20 and x<500:
   .....:             pyplot.text(x, y, str(x)[:6], fontsize=7, color='black')
   .....:     pyplot.xlabel(r"$1/f$")
   .....:     plt.savefig(name[0:-4]+'_fourier.png', bbox_inches='tight')           
   .....:     plt.clf()       
   .....:     df1 = pd.DataFrame()
   .....:     df1 = pd.DataFrame(data[:500])
   .....:     df1 = df1.T
   .....:     dfcaim = dfcaim.append(df1)
   .....:     #print len(data), frames, s[0:30]
   .....:     print dfcaim.shape







