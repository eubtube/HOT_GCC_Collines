# HOT_GCC_Collines
Automation Scripts for QGIS Project Creation

About:
----------------------
This repo contains scripts (in progress) for creating QGIS projects to be
used for the digitization of "collines" (hills) in Eastern DRC and Western
Uganda.

What's Inside:
----------------------
In the `docs` folder, you'll find a link to the Google Doc with the high level
overview of tasks done and to be done for this project. That's a good place to
start. Also included is a tutorial doc for how to do the digitization once a
project is set up.

In the `core_files` folder, you'll find four core files for the project:

- `create_projects.sh`: the main script that will iterate through lists of
3x3 groups of tiles. This currently has several placeholders in it that need
to be resolved, detailed in the "Issues".

- `add_to_qgisproject.py`: this code takes the files needed for each project
and adds them to an empty 3D enabled QGIS project. Everything should work as
is, with the exception of setting the extent, which worked as an indvidual
command in the QGIS Py console, but did not work in the overall script. This
has been opened as an issue.

- `iterate_grid.ipynb`: A Jupyter notebook where I
am attempting to set up a way to interate through a 31/30 grid going three
columns and three columns at a time to determine if there is an associated
Maxar tile in these cells.  If there are associated Maxar tiles in any of
the cells of the smaller 3x3 grid iteration, those quadkey codes would be
saved into a new text file. Each 3x3 grid iteration would also need a unique
ID that would be fed into a list of all the smaller grids (as a .txt) that
would then be iterated through in the `create_projects.sh` script to make
the directories and projects. **requires the `colline_grid_joined_adj.gpkg` from
the `files` folder**

- `gdal_stuff.sh` is simply a list of the `GDAL` snippets that are used in
`create_projects.sh` file above.

- In the `scratch` folder within, you'll find `Grid Value and Geopandas Exploration.ipynb`,
a very messy Jupyter Notebook where added the row and column fields to the 
intermediary `colline_grid_joined.gpkg` file and saved it as the final 
`colline_grid_joined_adj.gpkg` which is included here

In the `files` folder, you will find some of the geospatial files needed to test
or view some of the scripts or QGIS projects for visualization.

Included:
- `Border.gpkg`: DRC polygon file (UTM 35S Projection)
- `maxar_tile_extents.gpkg`: A polygon file with the footprints of the Maxar tiles
for the region
- `maxar_collines.gpkg`: Polygon file with the footprints for the colline regions
- `colline_extent.gpkg`: Extent of colline areas used to clip the colline extent
file above.
- `colline_grid_joined_adj.gpkg`: a grid based on the colline extents file above.
Grid draped over the entire colline area and a row/column location associated
with each cell that can ultimately be associated with a quadkey for the tile ID.
**for use with the `iterate_grid.ipynb` file to break
break the grid into projects**
- `102022.prj`: Esri projection file for Africa Albers projection
- `colline_grids.qgs`: a QGIS project for viewing the colline tile extents and the grid
for visualization of files for `iterate_grid.ipynb`.
- `3d_template_clean.qgs`: a QGIS project for testing `add_to_qgisproject.py`

Not Included (but needed for the scripts):
- The single JAXA file for the entire AOI in Africa Albers Projections used to make smaller project DEMs (about 5GB)
- Maxar Images (too big to share, but can share a sample)[150+ GB]
- DRC-UG Building Footprints (3.1 GB)


Still learning best practices for organizing repos and I'm aware this is quite a
mess, so I'm welcome to suggestions on how to better organize this into folders
