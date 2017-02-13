//
//Author: Csaba Veraszto
//Jekely lab MPI for Developmental Biology
//2014-2016

G_Ddir=getDirectory("Choose destination folder");
G_Sdir=getDirectory("Choose the directory where the files are");
list=getFileList(G_Sdir);
Array.sort(list);

setBatchMode(true);                    //You can uncheck this if you want to see the process. It will be slower. 
for (k=0; k<list.length; k++) {
	fullpath_image=G_Sdir + list[k];

	if (endsWith(fullpath_image, "lif")) {
	//open(fullpath_image);
	run("Bio-Formats Importer", 
	"open=fullpath_image autoscale color_mode=Grayscale split_channels open_all_series display_metadata view=Hyperstack stack_order=XYCZT"); //you can add  display_metadata to get more information pop up

	selectWindow("Original Metadata - "+list[k]);
	saveAs("Text", fullpath_image+"Original_Metadata.txt");
	run("Close");
	
	metadata=File.openAsString(fullpath_image+"Original_Metadata.txt");
	x1 = indexOf(metadata, "FrameTime");
	x2 = indexOf(metadata, "ATLConfocalSettingDefinition|Immersion");
		
	if (x1>x2) {
		x2 = x1+31;
		Speed = substring(metadata, x1+10, x2-1);
	}
	
	if (x1 ==-1) //This is a zstack.
		Speed = ("XYZ"); 
	else 
		Speed = substring(metadata, x1+10, x2-1);

		Speed=split(Speed, "\n");
		Speed=(Speed[0]);
		
		for (count=0; count<nImages; count++) {
		img_title = getTitle();
		selectWindow(img_title);
			
			if (endsWith(img_title, "C=1")) {		
				run("Enhance Contrast", "saturated=0.35");
				dest_filename= img_title + "_DIC" +".tif";
				fullpath_results = G_Ddir + dest_filename;
				saveAs("Tiff", fullpath_results);
				close;
			}
			
			img_title = getTitle();
		    selectWindow(img_title);
			if (endsWith(img_title, "C=0")) {
			run("Median...", "radius=2 stack");
			r=newArray(256);g=newArray(256);b=newArray(256); 
				for (i=0;i<256;i++) { 
					i4=4*i/256; 
					r[i]=255*minOf(maxOf(minOf(i4-1.5,-i4+4.5),0),1); 
					g[i]=255*minOf(maxOf(minOf(i4-0.5,-i4+3.5),0),1); 
					b[i]=255*minOf(maxOf(minOf(i4+0.5,-i4+2.5),0),1); 
				} 
				setLut(r,g,b); 
			
				dest_filename= img_title + "_processed_gcamp_dt_" + Speed + ".tif";
				fullpath_results = G_Ddir + dest_filename;
				saveAs("Tiff", fullpath_results);
				close;	
			}	
		}
	}
}
			