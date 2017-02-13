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
	
	if (endsWith(fullpath_image, "oib")) {
		//open(fullpath_image);
		run("Bio-Formats Importer", 
		"open=fullpath_image autoscale color_mode=Grayscale split_channels view=Hyperstack stack_order=XYCZT"); //you can add  display_metadata to get more information pop up
		
		img_title = getTitle();
		// Splitting channels for .lsm files
		//if ("Channels" >=2) {
		//run("Split Channels");
		//} 
		
		
		//Creating tiff file with transmitted channel only
		//name0=getTitle;
		//print(name0);
		selectWindow(img_title);
		
		//run("Descriptor-based series registration (2d/3d + t)", "series_of_images=img_title brightness_of=[Interactive ...] approximate_size=[Interactive ...] type_of_detections=[Interactive ...] transformation_model=[Rigid (2d)] number_of_neighbors=3 redundancy=1 significance=3 allowed_error_for_ransac=5 global_optimization=[All-to-all matching with range ('reasonable' global optimization)] range=5 choose_registration_channel=1 image=[Fuse and display]");
		//selectWindow(img_title);
		//close;
		
		run("Enhance Contrast", "saturated=0.35");
		dest_filename= img_title + "_DIC" +".tif";
		fullpath_results = G_Ddir + dest_filename;
		saveAs("Tiff", fullpath_results);
		close;
		
		img_title = getTitle();
		Speed = Stack.getFrameInterval();
		//run("Descriptor-based series registration (2d/3d + t)", "series_of_images=img_title reapply");
		//name1=getTitle;
		//Create temporal average
		//n = nSlices-1;
		//rename("stack");
		//run("Duplicate...", "title=stack-1 duplicate range=1-n");
		//selectWindow("stack");
		//run("Delete Slice");
		//imageCalculator("Average create stack", "stack","stack-1");
		//selectWindow("stack");
		//close();
		//selectWindow("stack-1");
		//close();
		//selectWindow("Result of stack");
		
		//Spatial filtering:
		run("Median...", "radius=2 stack");
		//run("Gaussian Blur...", "sigma=0.1 stack");
		
		
		//JET-LUT coloring
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