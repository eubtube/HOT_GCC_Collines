#!/bin/bash

# This script sets up the structure for the folders of each 3D project and running operations.
# TODO: Replace placeholders, give correct working directories.
# See if there is a way to pass ids through with quotes around path name (something like 'path for python')

echo creating the folders
cd /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/ #navigate to a folder for outputs
for i in [list of all "projects"]; do
    echo $i # This should be the project ID
    # cd ~/Documents/test  # set your output folder in this line, prob don't need
    y=$( echo $i | sed -r "s/(.+)\..+/\1/" ) # This removes the file extension for the folder name

    echo Starting $y
    mkdir $y

    cd $y

    mkdir "Raster"
      cd Raster
      cp tiles_$i.txt # list of tiles for that project, include extension to where those files are
      while read j; do
        echo Converting and Copying $j
        # Convert tiles to Africa Albers and send to file
        gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
         -r near -of GTiff -co COMPRESS=JPEG -co JPEG_QUALITY=75 -co PHOTOMETRIC=YCBCR\
          /media/eubtube/Seagate\ Backup\ Plus\ Drive/Congo_Tifs/raster/GeoTIFF/$j.tif\
           $j.tif
      done < tiles_$i.txt # file from above, should have the project id name
      cd ..

    mkdir "Vector"
      cd Vector
      cp $i_aoi.gpkg # from file with all aois OR insert python script here that creates AOI from tile names and places here.
      cp '/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/vector/Border.gpkg' . #change to vector file in github
      # Clip Buildings to Project AOI
      ogr2ogr -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\ # change path
       -clipsrc $i_aoi.gpkg -f 'GPKG' -overwrite $i_buildings.gpkg /home/eubtube/Documents/DRC-Uganda_Collines_3D/\
      Vector/2019_Maxar_Ecopia_DRC-Uganda_building_footprints.gpkg # change path
      cd ..

    cp /home/eubtube/Documents/colline_automation/files/3d_template_clean.qgs #change path

    cd Raster
      # Clip DEM to Project AOI
      gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
       -of GTiff -cutline /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/$i/Vector/$i_aoi.gpkg\
        -cl aoi -crop_to_cutline -co COMPRESS=LZW -co TILED=YES\
         "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged.tif"\
          $i_dem.tif
    cd ..

    python3.6 add_to_qgisproject.py -vd '/media/eubtube/Seagate Backup Plus Drive/Projects/SW_UG_1/Vector'\
     -rd /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/$i/Raster\
     -prid $i\
     -pd /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/$i\
     -qt /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/SW_UG_1/3d_template_clean.qgs # pass any arguments that will be necessary
    # also ensure that QGIS installation of Python is being used
done

echo finished

###########################################################################################

# Overall Workflow
# 1) create the AOI & Place in Vector folder
  # Do with python when pulling the tile IDs from `Grid Value and Geopandas Exploration.ipynb`
  # Search for col, row then throw range of all vals into a txt file

# 2) Clip the DSM to the AOI and place result in Raster folder
gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
 -of GTiff -cutline /media/eubtube/Seagate\ Backup\ Plus\ Drive/Projects/kisoro_5/Vector/aoi.gpkg\
 -cl aoi -crop_to_cutline -co COMPRESS=LZW -co TILED=YES\
 "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged.tif"\
 kisoro_5_dem.tif

# 3) Clip the buildings to the AOI and place result in Vector folder
    # Might need to break down the buildings into more manageable chunks as it takes a little while to cut
ogr2ogr -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\ # adjust to
 -clipsrc aoi.gpkg -f 'GPKG' kisoro_2_buildings.gpkg /home/eubtube/Documents/DRC-Uganda_Collines_3D/\
Vector/2019_Maxar_Ecopia_DRC-Uganda_building_footprints.gpkg

# 4) Manipulate HTML file to include all the new outputs in the QGIS File
    # PyQGIS api to place files into empty qgis 3D project (see `add_to_qgisproject.py`)
