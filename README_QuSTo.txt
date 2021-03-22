                                                               
  ,ad8888ba,                  ad88888ba  888888888888          
 d8"'    `"8b                d8"     "8b      88               
d8'        `8b               Y8,              88               
88          88  88       88  `Y8aaaaa,        88   ,adPPYba,   
88          88  88       88    `"""""8b,      88  a8"     "8a  
Y8,    "88,,8P  88       88          `8b      88  8b       d8  
 Y8a.    Y88P   "8a,   ,a88  Y8a     a8P      88  "8a,   ,a8"  
  `"Y8888Y"Y8a   `"YbbdP'Y8   "Y88888P"       88   `"YbbdP"'   
                                                               
                                                               

Thank you for downloading the QuSTo V1.0 application. This readme file provides information regarding the use of the application as well as about its background. 



1 - Using QuSTo V1.0

QuSTo, a versatile, open-source program developed in Python to quantify surface topography from 2D profiles. The program calculates metrics that quantify surface roughness and the size (i.e. height and length) and shape (i.e. convexity constant (CC), skewness (Sk), and kurtosis (Ku)) of surface structures. Currently, QuSTo only runs in the Windows operating system. 

The QuSTo application includes a Graphical User Interface (GUI). The application must be run in the particular sequence shown in the GUI, which is: 1) Load a File, 2) Structure Segmentation, and 3) Calculate.  

Load a file: Clicking the "Open File" button prompts a browser for the user to choose a .csv file. Clicking the "Load" button generates the Main Profile. Note that the convexity constant is only calculated on the left side of the structures. Thus, the user may need to "Flip" the profile. After selecting the "Flip" box, click the "Load" button again.

Structure Segmentation: An automatic segmentation option is implemented in the QuSTo application. Successfully segmenting the individual structures in the profile is an iterative process controlled by the value of the "Sensitivity" parameter. A sensitivity value of 1.5 is recommended, but the user should increase the sensitivity value if multiple structures are grouped together or decrease the sensitivity value if structures segmented into too many parts. After the sensitivity value is selected, the user should click the “Auto” button. The “Auto” button should be clicked every time the sensitivity value is changed. 

Calculate: Calculation of the shape parameters is performed once the user clicks the "Calculate" button. The "Acceptable Jump Range" is a filter for the user to avoid calculation of partial structures or structures whose shape is influenced by the overall profile shape. The "Jump" value is defined as the ratio of the difference in y coordinate between the first and last point of the profile to the structure height. Note that QuSTo does not report the shape parameters of the structures with "Jump" values outside the specified range. Note also that the units of the surface roughness, asperity height, and asperity length, as well as of the main profile plotted, are the same units in the input file for QuSTo. 

Once the above-described sequence has been completed, the user can use the drop-down menu on the bottom left side of the GUI to visualize individual structure profiles and inspect the corresponding shape parameters. 

The user can export the calculated structure shape parameters by clicking the "Export Table" button. After doing so, QuSTo prompts the user to select a directory location to save the exported .csv file. 

Six example files can be downloaded from the GitHub site for users to get familiar with the QuSTo application. 



2 - Input file format

The QuSTo application accepts files in .csv format. The file should contain two strings of data, the first one containing the x-coordinates of the profile and the second one containing the z (or y)-coordinates of the profiles. The first element of each column is a label such as "X (units)" and "Z (units)"

The shape parameters for each structure can be exported in .csv format.



3 - Background for calculation of shape parameters

For detailed information regarding the equations, data handling steps used to calculate the shape parameters (i.e. asperity height, asperity length, profile average surface roughness, convexity constant, skewness, and kurtosis), and examples, refer to the journal paper Martinez et al. (2020). 

Note also that the units of the surface roughness, asperity height, and asperity length, as well as of the main profile plotted in the GUI, are the same units in the input file for QuSTo. 

The surface roughness of the entire profile is quantified by means of the average surface roughness parameter (ISO 4287, 1997; Whitehouse, 2004). 

In order to quantify the size and shape individual surface structures, the profile must first be segmented to extract the individual structures. The QuSTo code segments individual structures in a 2D elevation profile using functions that locate the local minimum points.

Then, the z coordinates of the individual scales are shifted so that all the values are positive. This is necessary to calculate 

The height of the surface structure is taken as the difference in z coordinate between the local minimum and maximum points, while the structure length is defined as the difference in x coordinate between the feature first and last points.

The convexity constant is determined by fitting a quadratic equation to the portion of the structure profile from its beginning to its maximum z coordinate. The CC is the second derivative of the fitted quadratic function.

To calculate the skewness and kurtosis parameters, a statistical distribution based on the structure's 2D profile must be created. This is done by repeating each x coordinate value a number of times equal to the corresponding z coordinate. To accomplish this, z coordinate values must be positive, integer numbers. 



4 - Using the sepperate QuSlicer module (OPTIONAL STEP)

The Input files described above can be obtained from any bio-imaging technique from using any software capable with the capability of generating elevation profiles from a 3D image.

However, users also have the option of using the included QuSlicer module to obtain 2D profiles from 3D images. The files created from QuSlicer can then be loaded and analyzed with QuSTo.

QuSlicer works by running a sequence of three functions that each take vertex data from the last: 1) sliceVerts, 2) skimSlice, and 3) smoothSlice

sliceVerts(verts, axis, floor, ceil) takes a ‘slice’ of vertices from a 3D mesh. Inputs: 'verts' inputs the base vertex data, 'axis' (‘x’ ‘y’ or ‘z’) chooses slice direction, 'floor' and 'ceil' (0.0-1.0) define the size and location of the slice (ex: setting floor = .1 and ceil = .2 keeps verts between the 10% and 20% mark along the range of the chosen axis).

skimSlice(verts, axis, skim) removes unwanted data from the top or bottom of a choosen axis. Inputs: 'verts' inputs the data from sliceVerts, 'axis' ('x’, ‘y’, ‘z’) chooses the axis to skim from, 'skim' (0.0-1.0) defines the ratio of vertices to be preserved from the slice along the choosen axis (a positive skim preserves the top %, while a negative preserves the bottom %). Multiple skimSlices can be used to further adjust the slice. (In the case of multiple ‘skims,’ the output from the previous skimSlice serves as the input 'verts'.)

smoothSlice(verts, smootSteps, scale) removes noise and smoothes. Inputs: 'verts' inputs the data from skimSlice, 'smoothSteps' (0-3) defines level of “smoothness” (via flattening local peaks and troughs), 'scale' is a multiple used to increase the X,Z resolution if the resulting data is too small for skew and kurtosis calculations in QuSTo (see above section).

QuSlicer is not an executable file like QuSTo, but can be run in python by using the following line of code (objects in [BRACKETS] are to be replaced by the user with the item described):

from QuSlicer import QuSlicer
import open3d as o3d
import matplotlib.pyplot as plt

meshPath = "[ENTER OR COPY/PASTE THE PATH NAME OF THE 3D IMAGE FILE (.obj, .stl, etc.)]"
mesh = o3d.io.read_triangle_mesh(meshPath)
print(mesh)
slicedVerts = QuSlicer.sliceVerts(mesh.vertices, [AXIS], [FLOOR], [CIEL])
skimmedVerts = QuSlicer.skimSlice(slicedVerts, [AXIS], [SKIM])
smoothedVerts = QuSlicer.smoothSlice(skimmedVerts, [STEPS], [SCALE])
QuSlicer.writeCSV(smoothedVerts,'[INPUT THE LOCATION TO SAVE THE .CSV FILE]', "[INPUT THE DESIRED FILE NAME]")

3D image files (stl) for Sling tailed Agama skin, Florida Mammoth molar and Sea snail shell are available at: https://ucdavis.box.com/s/vt7l8sfe86cj0xb4xer6g9u60t3kcbyz

5 - References

ISO-4287. (1997). Geometrical Product Specifications (GPS) — Surface texture: Profile method — Term, definitions and surface texture parameters. Geneva, Switzerland.
Martinez, Nguyen, Basson, Irschick, Baeckens, and Medina (2020). Quantifying surface topography of biological systems from 3D scans. Submitted for possible publication at Methods in Ecology and Evolution. 
Whitehouse (2004). Surfaces and their measurements. Oxford: Butterworth-Heinemann.
