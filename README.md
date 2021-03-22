[![DOI](https://zenodo.org/badge/350409561.svg)](https://zenodo.org/badge/latestdoi/350409561)

# QuSTo : **Qu**antifying **S**urface **To**pography                                                       

QuSTo, a versatile, open-source program developed in Python to quantify surface topography from 2D profiles. The program calculates metrics that quantify surface roughness and the size (i.e. height and length) and shape (i.e. convexity constant (CC), skewness (Sk), and kurtosis (Ku)) of surface structures. Currently, QuSTo is available as a Windows executable, which neatly packs a python interpreter and the all the computational packages. The accompanying QuSlicer module gives users and optional way to obtain 2D profiles from 3D images. The files created from QuSlicer can then be loaded and analyzed with QuSTo. 

## Using the code

1. Either clone the repository (https://github.com/GMLatUCD/QuSTo.git) or download the zip file containing the executable QuSTo file, the python code for the QuSlicer module, and six trial surfaces.
2. Please read the README_QuSTo file as it contains all the information regarding the background and usage of the code and accompanying trial surfaces.
3. Double click on QuSTov1.0final executable file to run the GUI. 
4. QuSTo reads .csv files containing x-z coordinate data of 2d profiles (see the README_QuSTo file). These files can be obtained from any bio-imaging technique from using any software capable with the capability of generating elevation profiles from a 3D image or from the included QuSlicer module.
5. The separate QuSlicer module is not a windows executable, but can be run as python code. (see more details in the README_QuSTo file)

## Words of caution

1. As a onefile python executable it might take a few seconds to run the GUI, depending on the machine.
2. Please follow the exact procedure, defined in README_QuSTo, for a successful run as currently the code contains minimal debug error codes.

## Planned releases/improvements

1. The complete python code and compiled executable for Windows with faster runtime.
2. Additional filetypes for input file (txt,csv,xlsx)
3. Manual selection of the maxima and minima.
4. Automatic screen resizing based on screen size.

QuSTo was created at the Granular Materials Lab by Damon Nguyen and Mandeep Singh Basson. QuSlicer was developed by Josh Medina.

Copyright (C) 2020 Granular Materials Lab
