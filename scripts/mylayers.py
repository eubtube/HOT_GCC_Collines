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

red_style = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0',
             'color': 'red',
             'joinstyle': 'bevel',
             'offset': '0,0',
             'offset_map_unit_scale': '3x:0,0,0,0,0,0',
             "offset_unit": 'MM',
             'outline_style': 'solid',
             'outline_color': 'red',
             'outline_width': '0.26',
             'outline_width_unit': 'MM',
             'style': 'no'}

yellow_style = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0',
                 'color': '255,158,23,255',
                 'joinstyle': 'bevel',
                 'offset': '0,0',
                 'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                 "offset_unit": 'MM',
                 'outline_style': 'dash dot',
                 'outline_color': 'yellow',
                 'outline_width': '0.26',
                 'outline_width_unit': 'MM',
                 'style': 'no'}
