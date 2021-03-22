# QuSlicer Notes and Readme
QuSlicer ver 0.5 for QuSTO
Josh Medina
Updated 1/19/2021

QuSlicer inputs XYZ from mesh file, outputs XZ (or XY, etc.) for QuSTo. 

3D image files (stl) for Sling tailed Agama skin, Florida Mammoth molar and Sea snail shell are available at: https://ucdavis.box.com/s/vt7l8sfe86cj0xb4xer6g9u60t3kcbyz

## Changelog

Ver 0.5
- sliceSkim has been reworked, and can take negative values to skim the reverse side of any axis
- smoothSlice has been reworked to take one 'smooth amount' input called smoothSteps.
- manual scale adjustment now preseent in smoothSlice
- slice range and scale is adjusted to fit QuSto requirements
- data offset to 0 for better post-skim visualization
- added X,Z header to csv output
- removed debug plots and deprecated functions


Ver 0.4
- Replaced rolling average with rolling median; less data loss and more speed
- Added findPeaks method to assist with noise reduction
- Added selectPeak and reduceValley step counter for manaully adjusting noise reduction
- Added demo files


## Workflow

1. sliceVerts(verts, axis, floor, ceil)
	- sliceVerts takes a 'slice' of vertices from a 3D mes
	- verts inputs the base vertex data from mesh
	- axis ('x' 'y' or 'z') chooses slice direction
	- floor and ceil (0.0-1.0) define the size and location of the slice. For example, floor .1 and ceil .2 would 'keep' any verts between the 10% and 20% mark along the total range of the chosen axis

2. skimSlice(verts, axis, skim)
	- skimSlice clarifies the slice by removing unwanted data from the top or bottom of any axis. Multiple skimSlices can be used to further adjust the slice. 
	- verts inputs the 'sliced' vertex data from sliceVerts. (Or in the case of multiple 'skims,' the output from the previous skimSlice.)
	- axis ('x', 'y', 'z') describes the axis to skim from, ideally the vertical axis when graphed'
	- skim (0.0-1.0) defines the ratio of vertices to be preserved from the slice along the axis. A positive skim preserves the top %, while a negative preserves the bottom %. 

3. smoothSlice(verts, smootSteps, scale)
	- smoothSlice removes noise from the Slice and smoothes the final result for better visualization in QuSto. 
	- verts inputs the 'skimmed' vertex slice from skimSlice
	- smoothSteps (0-3) defines level of "smoothness" applied to verts via the flattening of local peaks and troughs.
	- scale is a simple multiple used to increase the X,Z resolution for use in QuSto, if need be.


- Example in main.py:
	- 03d loads the Sling Tailed Agama mesh found in meshPath
	- sliceVerts slices verts between 40% and 50% of the x-width.
	- skimVerts retains or 'skims' the slice's top 10% and removes the rest
	- smoothVerts removes noise from overlapping points, then smoothes the remainder via spline
	- writeCSV writes the output into the project documents folder



## Loose Ends


> o3d is very picky, and doesn't read some files. 

> spline doesn't form when there are duplicate vertices. Figure out a failsafe. 

> smoothSlice needs to distribute its 'resolution' vertices evenly along the spline's total distance, instead of evenly along the X axis. It tends to lose resolution during long vertical jumps along the spline.

> locating the slice is largely trial and error and isn't suited for text input. Place via sliders?

> quantifying the 'noise' from overlapping vertices may assist with slice placement





