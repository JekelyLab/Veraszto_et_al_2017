//export ROIs and text images for correlation analysis in python
//Gaspar Jekely, MPI for Developmental Biology, Tübingen
//Oct 2015

//In your working directory make a folder with four subfolders: ROIs, Text_Images, output_images, raw_video
//Select a Ca-imaging video and save it to raw_video (Optional: Scale down the video ~128x128, 8-bit stack to be faster)
//Define the ROIs manually and add them to the ROI manager 
//Run the ImageJ Macro ImageJ_saving_Script.ijm


macro "export ROIs and text images for correlation analysis in python"
 
{

No_ROIs=6 //set the number of ROIs to export
Video_Length=400 //set the number to the number of frames to analyse

run("Set Measurements...", "  mean redirect=None decimal=3");
G_Ddir_ROI=getDirectory("Choose destination folder for ROIs");
G_Ddir_TI=getDirectory("Choose destination folder for Text Images");
rename("stack");

run("Measure");
selectWindow("Results");
IJ.deleteRows(0, 1000000);


for (k=0; k<No_ROIs; k++)
{
	roiManager("Select", k);
	setSlice(1);
	for (j=0; j<Video_Length; j++) 
		{	
		run("Measure");
		run("Next Slice [>]");
				}
	selectWindow("Results");
	//IJ.deleteRows(0, j);
	dest_filename= "ROI_res"+k+".txt";
	fullpath_results = G_Ddir_ROI + dest_filename;
	saveAs("Text", fullpath_results);
	IJ.deleteRows(0, j);
			
}



//Video_Length=300 //set the number to the number of frames to analyse
//G_Ddir_TI=getDirectory("Choose destination folder for Text Images");
//img_title = getTitle();

{
	setSlice(1);
		for (j=0; j<Video_Length; j++) 
		{
			run("Select All");
			dest_filename= "stack_"+j;
			fullpath_results = G_Ddir_TI + dest_filename;
			saveAs("Text image", fullpath_results);
			run("Next Slice [>]");
		}
	}
}
 
