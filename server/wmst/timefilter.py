# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"
__license__ = "GPLv3"

import sys
import os

from qgis.server import *
from qgis.core import *
from qgis.PyQt.QtCore import QDateTime


class TimeFilter(QgsServerFilter):

    def __init__(self, serverIface):
        super().__init__(serverIface)

    def requestReady(self):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap()

        if 'LAYERS' not in params:
            return

        if 'TIME' not in params:
            params['TIME'] = '2020-08'  # default date

        dt = QDateTime.fromString(params['TIME'], "yyyy-MM").date()
        project = QgsConfigCache.instance().project(params['MAP'])

        gp = project.layerTreeRoot().findGroup(params['LAYERS'])
        if not gp:
            return

        for tree_layer in gp.findLayers():
            layer = tree_layer.layer()
            if layer.type() != QgsMapLayer.RasterLayer:
                continue

            prop = layer.temporalProperties()
            begin = prop.fixedTemporalRange().begin().date()

            if begin.year() != dt.year() or begin.month() != dt.month():
               continue

            request.setParameter('LAYERS', layer.name())

    def sendResponse(self):
        pass

    def responseComplete(self):
        pass
