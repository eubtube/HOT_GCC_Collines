#!/bin/python3.6

import sys, os

import pdb
import argparse
import mylayers

from qgis.PyQt.QtCore import (
    QRectF,
)

from qgis.core import *
'''
(
    QgsProject,
    QgsApplication,
    QgsLayerTreeModel,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsVectorLayer,
    QgsFillSymbol,
    QgsDataSourceUri,
    QgsCategorizedSymbolRenderer,
    QgsClassificationRange,
    QgsPointXY,
    QgsProject,
    QgsExpression,
    QgsField,
    QgsFields,
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureRenderer,
    QgsGeometry,
    QgsGraduatedSymbolRenderer,
    QgsMarkerSymbol,
    QgsMessageLog,
    QgsRectangle,
    QgsRendererCategory,
    QgsRendererRange,
    QgsSymbol,
    QgsVectorDataProvider,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsSpatialIndex,
    QgsVectorLayerUtils
)
'''

from qgis.core.additions.edit import edit

from qgis.PyQt.QtGui import (
    QColor,
)

from qgis.gui import (
    QgsLayerTreeView,
    QgsMapCanvas,
    QgsVertexMarker,
    QgsMapCanvasItem,
    QgsRubberBand,
)

###### Add Vector Layers

# Add and style buildings
def add_vector_layers(project, qpid, pathv):
    '''adds building, border layer to qgis project, returns building layer'''
    #print(pathv)
    buildingfile = os.path.join(pathv, '{}_buildings.gpkg'.format(qpid)) # not very functional, assumes knowledge that user might not. Make an optional parameter
    print(buildingfile)
    building_layer = QgsVectorLayer(buildingfile, "Buildings", "ogr") # accepts a geopackage, returns a layer
    if not building_layer or not building_layer.isValid():
        print("Building layer failed to load!")

    # adds layer to the canvas
    #QgsProject.instance().addMapLayer(building_layer, True)
    project.addMapLayer(building_layer, True)

    # Verifies that layer was read
    print(building_layer.displayField())

    print(mylayers.red_style)
    building_symbol = QgsFillSymbol.createSimple(mylayers.red_style)
    print(building_symbol)
    #renderer1 = building_layer.renderer().setSymbol(symbol)
    #pdb.set_trace()
    #print(dir(renderer1))
    building_layer.renderer().setSymbol(building_symbol)
    building_layer.triggerRepaint()

    # Add and style border layer
    borderfile = os.path.join(pathv, 'border.gpkg|layername=border')
    border_layer = QgsVectorLayer(borderfile, "Border", "ogr")
    if not border_layer or not border_layer.isValid():
        print("Border layer failed to load!")

    # adds layer to the canvas
    #QgsProject.instance().addMapLayer(border_layer, True)
    project.addMapLayer(border_layer, True)

    # Verifies that layer was read
    print(building_layer.displayField())

    print(mylayers.yellow_style)
    border_symbol = QgsFillSymbol.createSimple(mylayers.yellow_style)
    print(border_symbol)
    border_layer.renderer().setSymbol(border_symbol)
    border_layer.triggerRepaint()

    # Returns building layer, border layer added to QGIS project only
    return building_layer

def set_extent(layer):
    '''Sets extent of QGIS canvas to a layer'''
    layer.selectAll()
    canvas = QgsMapCanvas()
    canvas.zoomToSelected(layer)
    layer.removeSelection()

######## Add Raster Layers
# TODO: Make general enough to add any raster layer, only pass in orthos
# select .tifs and filter out dem in "build_proj"
def add_tile_group(project, root, pathr, group_name):
    '''adds project Maxar tiles to QGIS project. var root is a layer tree '''
    # Set up Tiles Group

    tiles_group = root.insertGroup(-1, group_name)

    # Adds just the Maxar tiles to the group
    for filename in os.listdir(pathr):
        if (filename.endswith('.tif')) & (('dem' in filename) == False): # grabs only files that do not have "dem" in their name
            tile = os.path.join(pathr, filename)
            # reads the raster layer object
            ortho_layer = QgsRasterLayer(tile, os.path.splitext(filename)[0])  # Os.path - get only extension
            #QgsProject.instance().addMapLayer(ortho_layer, False)
            project.addMapLayer(ortho_layer, False)
            root.insertChildNode(-1, QgsLayerTreeLayer(ortho_layer))
            node_ortho_layer = QgsLayerTreeLayer(ortho_layer)
            tiles_group.insertChildNode(0, node_ortho_layer)
            root.removeLayer(ortho_layer)
        else:
            pass


# Adds the DEM below
# TODO: combine with function above, make add raster layers
def add_dem(project, root, qpid, pathr):
    ''' '''
    dem = os.path.join(pathr, '{}_dem.tif'.format(qpid))
    dem_layer = QgsRasterLayer(dem, '{}_dem'.format(qpid))
    #QgsProject.instance().addMapLayer(dem_layer, False)
    project.addMapLayer(dem_layer, False)
    root.insertChildNode(-1, QgsLayerTreeLayer(dem_layer))


''' Don't seem to be able to set up a 3D view with current bindings...
# Set up 3D view
Qgs3D.initialize()
'''
def build_proj(qpid, pdir, pathv, pathr, template):

    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    qgs = QgsApplication([], False) # "False" prevents the gui from opening
    qgs.initQgis()

    # Will need to start a project
    project = QgsProject.instance()
    project.read(template) # How to generalize this??  May be OK

    # Creates a layer tree in the QGIS project called root
    #root = QgsProject.instance().layerTreeRoot()
    root = project.layerTreeRoot()

    # Adds vector layers
    building_layer = add_vector_layers(project, qpid, pathv)

    # Sets extent to building layer
    set_extent(building_layer)

    # Adds all tiles as a grouped file in TOC
    add_tile_group(project, root, pathr, "Tiles")

    # Adds DEM below Tiles
    add_dem(project, root, qpid, pathr)

    # Prints what's in the project
    print(QgsProject.instance().mapLayers().values())

    # Write to the QGIS Project, commented out when testing to avoid overwriting blank file
    project.write()

    # Exit QGIS
    qgs.exitQgis()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-vd", "--vector_directory", help = "Directory path containing your vector files.")
    parser.add_argument("-rd", "--raster_directory", help = "Directory path containing your raster files.")
    parser.add_argument("-prid", "--project_id", help = "Your project ID.")
    parser.add_argument("-pd", "--project_directory", help = "Directory path containing all you project files.")
    parser.add_argument("-qt", "--qgis_template", help = "QGIS project template")

    options = parser.parse_args()
    #print(options)
    #print(type(options))

    build_proj(options.project_id, options.project_directory, options.vector_directory, options.raster_directory, options.qgis_template)
