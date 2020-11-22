#!/bin/python3.6

import os
from qgis.core import *
import os, sys

"""
QgsProject, QgsLayerTreeGroup, QgsLayerTreeLayer, QgsVectorLayer,QgsLayerTreeModel
"""


###### Add Vector Layers

# Add and style buildings
def add_vector_layers(id):
    layer1 = iface.addVectorLayer(pathv + str(id) + "_buildings.gpkg", "Buildings", "ogr")
    if not layer1 or not layer1.isValid():
        print("Layer failed to load!")

    layer1 = iface.activeLayer()
    symbol = QgsFillSymbol.createSimple({'border_width_map_unit_scale': '3x:0,0,0,0,0,0',
                                         'color': 'red',
                                         'joinstyle': 'bevel',
                                         'offset': '0,0',
                                         'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                         "offset_unit": 'MM',
                                         'outline_style': 'solid',
                                         'outline_color': 'red',
                                         'outline_width': '0.26',
                                         'outline_width_unit': 'MM',
                                         'style': 'no'})
    layer1.renderer().setSymbol(symbol)
    layer1.triggerRepaint()

    # Add and style border
    layer2 = iface.addVectorLayer(pathv + "Border.gpkg|layername=Border", "Border", "ogr")
    if not layer2 or not layer2.isValid():
        print("Layer failed to load!")

    layer2 = iface.activeLayer()
    symbol = QgsFillSymbol.createSimple({'border_width_map_unit_scale': '3x:0,0,0,0,0,0',
                                         'color': '255,158,23,255',
                                         'joinstyle': 'bevel',
                                         'offset': '0,0',
                                         'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                         "offset_unit": 'MM',
                                         'outline_style': 'dash dot',
                                         'outline_color': 'yellow',
                                         'outline_width': '0.26',
                                         'outline_width_unit': 'MM',
                                         'style': 'no'})
    layer2.renderer().setSymbol(symbol)
    layer2.triggerRepaint()

# Sets the extent to the clipped buildings

def set_extent(layer1):
    layer1 = iface.activeLayer()
    layer1.selectAll()
    canvas = iface.mapCanvas()
    canvas.zoomToSelected(layer1)
    layer1.removeSelection()

######## Add Raster Layers

def add_tile_group():
    # Set up Tiles Group
    layerTree = iface.layerTreeCanvasBridge().rootGroup()
    root = QgsProject.instance().layerTreeRoot()
    tiles_group = root.insertGroup(-1, "Tiles")

    # Adds just the tiles to the group
    for filename in os.listdir(pathr):
        if (filename.endswith('.tif')) & (('dem' in filename) == False): # only files that do not have "dem in their name"
            rlayer = QgsRasterLayer(pathr + filename, filename.strip('.tif'))  # Os.path - get only extension
            QgsProject.instance().addMapLayer(rlayer, False)
            layerTree.insertChildNode(-1, QgsLayerTreeLayer(rlayer))
            node_rlayer = QgsLayerTreeLayer(rlayer)
            tiles_group.insertChildNode(0, node_rlayer)
            root.removeLayer(rlayer)
        else:
            pass


# Adds the DEM below
def add_dem(id):
    dem = id + '_dem.tif'
    dem_layer = QgsRasterLayer(pathr + dem, dem.strip('.tif'))
    QgsProject.instance().addMapLayer(dem_layer, False)
    layerTree.insertChildNode(-1, QgsLayerTreeLayer(dem_layer))


''' Don't seem to be able to set up a 3D view with current bindings...
# Set up 3D view
Qgs3D.initialize()
'''
def build_proj(id, ):
    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    qgs = QgsApplication([], False) # "False" prevents the gui from opening
    qgs.initQgis()

    ProjectName = str(id) + ".qgs"

    # Will need to start a project
    project = QgsProject.instance()
    project.read('~/files/3d_template_clean.qgs') # How to generalize this??

# Might need to initate qgis when working from Bash



# project_path = QFileInfo(ProjectName)

pathv = '~/Projects/' + id + '/Vector/'
pathr = '~/Projects/' + id + '/Raster/'

#canvas = iface.mapCanvas()

# Write to the QGIS Project, commented out when testing to avoid overwriting blank file
project.write('/home/eubtube/Documents/colline_automation/3d_template_clean.qgs')

# Exit QGIS
qgs.exitQgis()
