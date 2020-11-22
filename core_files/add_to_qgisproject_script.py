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

#ProjectName = "sw_ug_1_test.qgs"

# Used to initate qgis when working from Bash
QgsApplication.setPrefixPath("/usr/bin/qgis", True)
qgs = QgsApplication([], False) # "False" prevents the gui from opening
qgs.initQgis()

# Will need to start a project
project = QgsProject.instance()
project.read('~/Documents/colline_automation/files/3d_template_clean.qgs')
# project_path = QFileInfo(ProjectName)

pathv = '/media/eubtube/Seagate Backup Plus Drive/Projects/SW_UG_1/Vector/'
pathr = '/media/eubtube/Seagate Backup Plus Drive/Projects/SW_UG_1/Raster/'


###### Add Vector Layers

# Add and style buildings
 # Creates layer1 variable
layer1 = QgsVectorLayer(pathv + "sw_ug_1_buildings.gpkg", "Buildings", "ogr")
if not layer1 or not layer1.isValid():
    print("Layer failed to load!")
# adds layer to the canvas
QgsProject.instance().addMapLayer(layer1, True)

print(layer1.displayField())

#layer1 = iface.activeLayer()
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

# Add and style border   Each of these as a function

layer2 = QgsVectorLayer(pathv + "border.gpkg|layername=border", "Border", "ogr")
if not layer2 or not layer2.isValid():
    print("Layer failed to load!")

QgsProject.instance().addMapLayer(layer2, True)

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

# Sets the extent to the clipped buildings - This is working
layer1.selectAll()
canvas = QgsMapCanvas()
canvas.zoomToSelected(layer1)
layer1.removeSelection()

######## Add Raster Layers

# Set up Tiles Group
root = QgsProject.instance().layerTreeRoot()
tiles_group = root.insertGroup(-1, "Tiles")

# Adds just the tiles to the group
for filename in os.listdir(pathr):
    if (filename.endswith('.tif')) & (('dem' in filename) == False):
        rlayer = QgsRasterLayer(pathr + filename, filename.strip('.tif'))  # Os.path - get only extension
        QgsProject.instance().addMapLayer(rlayer, False)
        root.insertChildNode(-1, QgsLayerTreeLayer(rlayer))
        node_rlayer = QgsLayerTreeLayer(rlayer)
        tiles_group.insertChildNode(0, node_rlayer)
        root.removeLayer(rlayer)
    else:
        pass


# Adds the DEM below
dem = 'sw_ug_1_dem.tif'
dem_layer = QgsRasterLayer(pathr + dem, dem.strip('.tif'))
QgsProject.instance().addMapLayer(dem_layer, False)
root.insertChildNode(-1, QgsLayerTreeLayer(dem_layer))


''' Don't seem to be able to set up a 3D view with current bindings...
# Set up 3D view
Qgs3D.initialize()
'''

print(QgsProject.instance().mapLayers().values())

# Write to the QGIS Project, commented out when testing to avoid overwriting blank file
#project.write('/home/eubtube/Documents/colline_automation/3d_template_clean_test.qgs')
project.write('/home/eubtube/Documents/colline_automation/files/3d_template_clean.qgs')

# Exit QGIS
qgs.exitQgis()
