# STSP
This application downloads information from NDVI, cuts the information for a specific country in a short period of time.

## Requirements
  - Python3

## Installations
```sh
   $ pip install numpy==1.16.2
   $ pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
```
#### *Parameters*
- s --start : From the year of which the data is required (Example: 2018-05).
- f --finish : Until the year the data is required (Example: 2019-06)
- c --country : Country code for cut the information 
- u --user : NASA Earthdata Username for app Daac2Disk_ubuntu 
- p --password : NASA Earthdata Password for app Daac2Disk_ubuntu 
- d --directory : Path of the folder "Countries" and "Data" 
- o --output : Path of the folder for save the .zip 
- v --version : Software version 
- h --help : Print this help

#### *Examples*
  ```sh
   $ python mainWeb.py -u 'YOURUSER' -p 'YOURPASSWORD' -d 'PATH/FOR/TEMP/DATA' -o 'PATH/FOR/OUTPUT/DATA'  -s '2019-03' -f '2019-04' -c 'do'
  ```
  
 ## Author
Brandon Madriz(b.madriz@cgiar.org / bmadriz@mrbotcr.com)
