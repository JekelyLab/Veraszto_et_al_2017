'''
Correlation analysis of calcium-imaging movies
Gaspar Jekely, MPI for Developmental Biology, Tübingen Oct 2015
Modified by Csaba Veraszto, MPI for Developmental Biology, Tübingen Dec 2016
It is a prerequisite to have 4 folders, the video you are analyzing has to be a square (e.g. 512x512, 128x128), otherwise the script won't work. 

'''

import numpy as np
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend. Important if you run it without needing an X-server.
import matplotlib.pyplot as plt # Import pyplot afterwards the previous line, otherwise you are in trouble
import os, os.path
from os import listdir
from os.path import isfile, join
from PIL import Image
import pandas as pd #Pandas is a must
import seaborn as sns #Only for nice graphs

df1 = pd.DataFrame() #define panda dataframes
df2 = pd.DataFrame() #Also clears the dataframes from data of previous runs


#Set the directory
Dir='/where/your/files/are/' #directory with the working folders
#You can also set the 3 important variables by hand: number_of_cells= number of ROIs (and output images), number_of_cell=number of frames of your video, image_size=size of your square shaped video
moviename = [movie for movie in listdir(str(Dir)+'raw_video/') if movie[0:1]!='.' in movie] #Grab the name of the first file (will get rid of OSX generated hidden files, but please have only one video in this folder)
image = Dir + 'raw_video/' + moviename[0]
im = Image.open(image)
#imarray = numpy.array(im)
image_size=im.size[0]
number_of_cells=len([name for name in os.listdir(str(Dir)+'ROIs/') if name[0:2]=="RO" in name]) #Counts how many ROIs you defined.
number_of_files = len([s for s in os.listdir(str(Dir)+'Text_Images/') if s[0:2]=="st" in s]) #Counts how many frames your video consisted.

#Import all text images representing frames of the movie, and create a big dataframe
for k in range(0, number_of_files):  #loop through file list
   .....:     df = pd.read_csv(filepath_or_buffer=str(Dir)+'Text_Images/stack_' + str(k) + '.txt', header=None, sep='\t')
   .....:     df1 = pd.DataFrame()
   .....:     df1= df[0]
   .....:     for x in range(1, image_size):
   .....:         df1=df1.append(df[x])
   .....:     df2=pd.concat([df2, df1], axis=1)    
   .....: df2=df2.T 

#Normalization by dividing with Max of each column is not necessary.
#df2Max= df2.max(axis=0)
#df2=df2.divide(df2Max)
#print "Done"

import scipy
from scipy import stats

#Import reference signal and create Text images and sns generated images with LUT plots. The for loop will generate 2 images (text + sns) for each ROI. 
print "Writing image:"
for m in range(0, number_of_cells):  #loop through file list
   .....:         reference = pd.read_csv(filepath_or_buffer=str(Dir)+'ROIs/ROI_res' + str(m) + '.txt', header=0, sep='\t')
   .....:         reference = reference.iloc[0:number_of_files,1] #truncate reference according to the number of files to analyze, also truncate first row "Mean"
   .....:         #Normalization by dividng with Max 
   .....:         Max= reference.max(axis=0)
   .....:         reference=reference.divide(Max)
   .....:         Pearson=pd.DataFrame() #Generates a 3rd dataframe, calculates Pearson correlation coeefficients.
   .....:         for n in range (0,image_size*image_size-1):
   .....:                 y=scipy.stats.pearsonr(df2.iloc[:,n], reference)
   .....:                 Pearson = np.append(Pearson,y[0])
   .....:             #Printing the image and formattin by braking up the correlation list to a table
   .....:         Pearson_image = np.zeros(image_size) 
   .....:         for l in range (0,image_size-1):
   .....:             y=(Pearson[image_size*l:image_size*l+image_size:1]) #Makes it 2D and changes the values
   .....:             if l<1:
   .....:                 Pearson_image=y
   .....:             Pearson_image = np.column_stack((Pearson_image, y)) #Final image   
   .....:         np.savetxt(str(Dir)+'/output_images/Pearson_image' + str(m) + '.txt', Pearson_image, delimiter=",") #Text image is saved, simply from the variable.
   .....:         plt.ioff()
   .....:         cmap = sns.diverging_palette(220, 10, as_cmap=True) #Creates the heatmap plot with 2 colors.
   .....:         ax = plt.subplots(figsize=(8, 7)) #Creates an image (size is 8 inch by 7 inch)
   .....:         sns.set_style("darkgrid", {'font.sans-serif': [u'Arial']})
   .....:         ax = sns.heatmap(Pearson_image, cmap=cmap, xticklabels=False, yticklabels=False, vmax=1, vmin=-1, square=True) #Creates the actual image. It makes sure it's a square image.
   .....:         plt.savefig(str(Dir)+'/output_images/Pearson_image' + str(m) + '.png', format='png', dpi=300, bbox_inches='tight', pad_inches=0, frameon=None, transparent=True)        
   .....:         plt.clf()
 
print "Next Please!"



