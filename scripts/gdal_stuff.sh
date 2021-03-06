#!/bin/bash

# GDAL Actions

################ Converting tiles to new EPSG ###################
# cd folder/with/project/tifs
cd /file/with/sample.txt

sample_tiles.txt

while read j; do
  echo Converting and Copying $j
  # Convert tiles to Africa Albers and send to file
  gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
  -r near -of GTiff -co COMPRESS=JPEG -co JPEG_QUALITY=75 -co PHOTOMETRIC=YCBCR\
  /media/eubtube/Seagate\ Backup\ Plus\ Drive/Congo_Tifs/raster/GeoTIFF/$j.tif\
  $j.tif
done < sample_tiles.txt



############### Clipping Jaxa tile to AOI and Converting EPSG ################

i = path/to/aoifolder

cd /home/eubtube/Documents/test/test_jaxa/Raster

# Combining the two processes below

gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
-of GTiff -cutline "~/Documents/test/test_jaxa/Vector/aoi_bunia_84.gpkg -cl aoi_bunia_84"\
-crop_to_cutline "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged.tif"\
aoitest_84.tif

# Separating them to test outputs

# Cropping to aoi

gdalwarp -of GTiff -cutline ~/Documents/test/test_jaxa/Vector/aoi_bunia_84.gpkg -cl aoi_bunia_84\
 -crop_to_cutline "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged.tif"\
  aoitest_84.tif

# Trying with All Africa Albers Projections to try to fix cutlines

gdalwarp -of GTiff -cutline ~/Documents/test/test_jaxa/Vector/aoi_bunia.gpkg\
  -crop_to_cutline -overwrite "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged_afalb.tif"\
   aoitest_afalb.tif

# for DSM of Uganda demo project
#gdalwarp -of GTiff -cutline ~/Documents/DRC-Uganda_Collines_3D/Vector/og_colline_footprint.gpkg\
#   -cl og_colline_footprint -crop_to_cutline "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/jaxa/jaxa_all_merged.tif"\
#   newdemtest.tif


# Change EPSG

gdalwarp -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj\
 -r near -of GTiff -co COMPRESS=JPEG -co JPEG_QUALITY=75 -co PHOTOMETRIC=YCBCR /home/eubtube/Documents/test/test_jaxa/Raster/aoitest_84.tif aoi_afalb.tif

#For UTM 36N
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:32735\
  -r near -of GTiff -co COMPRESS=JPEG -co JPEG_QUALITY=75 -co PHOTOMETRIC=YCBCR\
  "/media/eubtube/Seagate Backup Plus Drive/Congo_Tifs/raster/GeoTIFF/102323230000.tif"\
  102323230000.tif

 # tried clipping 2 ways, transforming from WGS84 to Africa Albers as I clipped, and transforming after clipping.
 # both yield some pretty weird cutline artifacts on the raster.  Seem to be from the

 ############### Clipping buildings to aoi #################
cd /home/eubtube/Documents/test/myesri/Vector
ogr2ogr -s_srs EPSG:4326 -t_srs ESRI::/home/eubtube/Documents/colline_automation/files/102022.prj -f 'GPKG' -overwrite bunia_buildings.gpkg /home/eubtube/Documents/DRC-Uganda_Collines_3D/Vector/2019_Maxar_Ecopia_DRC-Uganda_building_footprints.gpkg -clipsrc /home/eubtube/Documents/test/test_jaxa/Vector/aoi_bunia.gpkg
