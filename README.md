# Veraszto_et_al_2017
ImageJ and python scripts from Veraszto et al 2017

Neuron activity analysis of calcium imaging videos:

The ImageJ/Fiji macro scripts (batch_for_LIF.ijm, batch_for_OIB.ijm, Saving_for_correlation_analysis.ijm) were used to export Leica LIF and Olympus OIB files for downstream calcium imaging analysis (Calcium-Imaging_batch.py) or to export calcium imaging data for ROIs for correlation analysis (correlation_analysis.py).

The batch_for_LIF.ijm and batch_for_OIB.ijm scripts will read LIF or OIB files and export the separate channels after median filtering, and LUT conversion. These files are the input for the Calcium-Imaging_batch.py Ca-imaging script. This script calculates dF/F, can be run in batch mode. Before running it, one has to set the path, the number of frames used to calculate the minimum for F0. Time is read from the input filenames. The plot has a fixed plt.ylim (y axis), which you might want to adjust, if the graph goes outside its range, but it allows you to produce equally sized images. 

Correlation analysis of calcium imaging videos:

The Saving_for_correlation_analysis.ijm script exports activity data for ROIs from calcium imaging videos. You need 4 folders, and a square video (e.g. 512x512, 128x128). In your working directory make a folder with four subfolders: ROIs, Text_Images, output_images, raw_video. Save the Ca-imaging video to raw_video (Optional: Scale down the video ~128x128, 8-bit stack to be faster). In ImageJ, define ROIs manually and add them to the ROI manager. Then run the Saving_for_correlation_analysis.ijm script.

Finally, run the correlation_analysis.py script. Include the path to your files.
