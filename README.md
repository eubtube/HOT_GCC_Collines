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

In the `scripts` folder, you'll find the three core files/scripts for the project:
    - `create_projects.sh`: the main script that will iterate through lists of
    3x3 groups of tiles. This currently has several placeholders in it that need
    to be resolved, detailed in the "Issues".
    - `add_to_qgisproject.py`: this code takes the files needed for each project
    and adds them to an empty 3D enabled QGIS project. Everything should work as
    is, with the exception of setting the extent, which worked as an indvidual
    command in the QGIS Py console, but did not work in the overall script. This
    has been opened as an issue.
    - `Grid Value and Geopandas Exploration.ipynb`: A Jupyter notebook where I
    am attempting to set up a way to interate through a 31/30 grid going three
    columns and three columns at a time to determine if there is an associated
    Maxar tile in these cells.  If there are associated Maxar tiles in any of
    the cells of the smaller 3x3 grid iteration, those quadkey codes would be
    saved into a new text file. Each 3x3 grid iteration would also need a unique
    ID that would be fed into a list of all the smaller grids (as a .txt) that
    would then be iterated through in the `create_projects.sh` script to make
    the directories and projects.
    - `gdal_stuff.sh` is simply a list of the `GDAL` snippets that are used in
    `create_projects.sh` file above.

In the `files` folder, y


Still learning best practices for organizing repos and I'm aware this is quite a
mess, so I'm welcome to suggestions on how to better organize this into folders
