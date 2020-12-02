#!/bin/python3.6

import sys, os

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
def add_vector_layers(qpid, pathv):
    layer1 = QgsVectorLayer(pathv + qpid  +"_buildings.gpkg", "Buildings", "ogr")
    if not layer1 or not layer1.isValid():
        print("Layer failed to load!")

    # adds layer to the canvas
    QgsProject.instance().addMapLayer(layer1, True)

    # Verifies that layer was read
    print(layer1.displayField())

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
    # Pulled from previous version:
    #renderer = layer1.renderer()
    #print("Type:", renderer.type())

    renderer1 = layer1.renderer().setSymbol(symbol)
    print(type(renderer1))
    print(dir(renderer1))
    #layer1.renderer().setSymbol(symbol)
    layer1.triggerRepaint()

    # Add and style border layer
    layer2 = QgsVectorLayer(pathv + "border.gpkg|layername=border", "Border", "ogr")
    if not layer2 or not layer2.isValid():
        print("Layer failed to load!")

    QgsProject.instance().addMapLayer(layer2, True)

    # Verifies that layer was read
    print(layer2.displayField())

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

    return(layer1)
    return(layer2)

# Sets the extent to the clipped buildings

def set_extent(layer1):
    layer1.selectAll()
    canvas = QgsMapCanvas()
    canvas.zoomToSelected(layer1)
    layer1.removeSelection()

######## Add Raster Layers

def add_tile_group(pathr):
    # Set up Tiles Group
    root = QgsProject.instance().layerTreeRoot()
    tiles_group = root.insertGroup(-1, "Tiles")

    # Adds just the tiles to the group
    for filename in os.listdir(pathr):
        if (filename.endswith('.tif')) & (('dem' in filename) == False): # only files that do not have "dem in their name"
            rlayer = QgsRasterLayer(pathr + filename, filename.strip('.tif'))  # Os.path - get only extension
            QgsProject.instance().addMapLayer(rlayer, False)
            root.insertChildNode(-1, QgsLayerTreeLayer(rlayer))
            node_rlayer = QgsLayerTreeLayer(rlayer)
            tiles_group.insertChildNode(0, node_rlayer)
            root.removeLayer(rlayer)
        else:
            pass


# Adds the DEM below
def add_dem(qpid, pathr):
    dem = qpid  + '_dem.tif'
    dem_layer = QgsRasterLayer(pathr + dem, dem.strip('.tif'))
    QgsProject.instance().addMapLayer(dem_layer, False)
    root.insertChildNode(-1, QgsLayerTreeLayer(dem_layer))


''' Don't seem to be able to set up a 3D view with current bindings...
# Set up 3D view
Qgs3D.initialize()
'''
def build_proj(qpid):
    pathv = '~/Projects/' + qpid  + '/Vector/'
    pathr = '~/Projects/' + qpid  + '/Raster/'

    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    qgs = QgsApplication([], False) # "False" prevents the gui from opening
    qgs.initQgis()

    # Will need to start a project
    project = QgsProject.instance()
    project.read('~/files/3d_template_clean.qgs') # How to generalize this??

    # Adds vector layers
    add_vector_layers(qpid, pathv)

    # Sets extent to building layer
    set_extent(layer1)

    # Adds all tiles as a grouped file in TOC
    add_tile_group(pathr)

    # Adds DEM below Tiles
    add_dem(qpid)

    # Prints the
    print(QgsProject.instance().mapLayers().values())

    # Write to the QGIS Project, commented out when testing to avoid overwriting blank file
    project.write()

    # Exit QGIS
    qgs.exitQgis()

if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)
    build_proj(sys.argv[1])
