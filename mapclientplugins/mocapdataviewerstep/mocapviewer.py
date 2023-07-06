'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide6 import QtCore, QtWidgets

from cmlibs.zinc.context import Context

from mapclientplugins.mocapdataviewerstep.ui_mocapviewer import Ui_MOCAPViewer
from mapclientplugins.mocapdataviewerstep.zincutils import createFiniteElementField, createNodeGraphics, \
    createStoredStringField


class MOCAPViewer(QtWidgets.QWidget):

    def __init__(self, trc_data):
        super(MOCAPViewer, self).__init__()
        self._trc_data = trc_data
        self._ui = Ui_MOCAPViewer()
        self._ui.setupUi(self)

        self._nodes = []
        self._labels = self._trc_data['Labels'][2:]
        frame_min = self._trc_data['Frame#'][0]
        frame_max = self._trc_data['Frame#'][-1]
        time_min = self._trc_data['Time'][0]
        time_max = self._trc_data['Time'][-1]

        self._ui.horizontalSlider.setMinimum(frame_min)
        self._ui.horizontalSlider.setMaximum(frame_max)

        self._ui.spinBox.setValue(10)

        self._context = Context('MOCAP')
        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()
        materialmodule = self._context.getMaterialmodule()
        materialmodule.defineStandardMaterials()
        self._ui.zincWidget.setContext(self._context)

        self._timer = QtCore.QTimer(self)
        self._timeKeeper = self._context.getTimekeepermodule().getDefaultTimekeeper()
        self._timeKeeper.setMinimumTime(time_min)
        self._timeKeeper.setMaximumTime(time_max)

        self._region = self._context.getDefaultRegion()
        self._createScene(self._region)
        self._graphics = createNodeGraphics(self._region)

        self._populateListWidget()
        self._makeConnections()

    def _makeConnections(self):
        self._ui.listWidget.itemClicked.connect(self._labelClicked)
        self._ui.listWidget.itemChanged.connect(self._labelChanged)
        self._ui.zincWidget.graphicsInitialized.connect(self._sceneviewerReady)
        self._ui.pushButtonPlay.clicked.connect(self._playClicked)
        self._ui.spinBox.valueChanged.connect(self._sizeChanged)
        self._ui.horizontalSlider.valueChanged.connect(self._timeChanged)
        self._timer.timeout.connect(self._timeIncrement)

    def _playClicked(self):
        text = self._ui.pushButtonPlay.text()
        if text == '&Play':
            self._timer.start(10)
            self._ui.pushButtonPlay.setText('&Stop')
        else:
            self._timer.stop()
            self._ui.pushButtonPlay.setText('&Play')

    def _timeIncrement(self):
        time_increment = 1
        current_value = self._ui.horizontalSlider.value()
        current_value += time_increment
        if current_value >= self._ui.horizontalSlider.maximum():
            current_value = self._ui.horizontalSlider.minimum()

        self._ui.horizontalSlider.setValue(current_value)

    def _sizeChanged(self, value):
        scene = self._region.getScene()
        scene.beginChange()
        for graphics in self._graphics:
            attributes = graphics.getGraphicspointattributes()
            attributes.setBaseSize(value)
        scene.endChange()

    def _timeChanged(self, frame_index):
        time = self._trc_data['Time'][frame_index - 1]
        self._timeKeeper.setTime(time)

    def _sceneviewerReady(self):
        self._ui.zincWidget.viewAll()

    def getTRCData(self):
        return self._trc_data

    def _getNodeForLabel(self, label):
        index = self._labels.index(label)
        node = self._nodes[index]

        return node

    def _labelClicked(self, item):
        # Set node selected.
        node = self._getNodeForLabel(item.text())
        nodeset = node.getNodeset()
        selection_group = self._ui.zincWidget.getSelectionGroup()
        group = selection_group.getOrCreateNodesetGroup(nodeset)
        if not group.containsNode(node):
            group.removeAllNodes()
            group.addNode(node)

    def _labelChanged(self, item):

        row = self._ui.listWidget.row(item)
        node = self._getNodeForLabel(self._labels[row])

        new_text = str(item.text())
        old_text = self._labels[row]

        fieldmodule = self._region.getFieldmodule()
        fieldcache = fieldmodule.createFieldcache()

        fieldmodule.beginChange()

        fieldcache.setNode(node)
        self._string_field.assignString(fieldcache, new_text)
        self._labels[row] = new_text
        self._trc_data[new_text] = self._trc_data.pop(old_text)
        self._trc_data['Labels'][row + 2] = new_text

        fieldmodule.endChange()

    def _populateListWidget(self):
        self._ui.listWidget.addItems(self._labels)
        for index in xrange(self._ui.listWidget.count()):
            item = self._ui.listWidget.item(index)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def _createScene(self, region):
        coordinate_field = createFiniteElementField(region)
        self._string_field = createStoredStringField(region)
        fieldmodule = region.getFieldmodule()
        fieldmodule.beginChange()
        nodeset = fieldmodule.findNodesetByName('nodes')
        node_template = nodeset.createNodetemplate()

        time = self._trc_data['Time']
        ts = fieldmodule.getMatchingTimesequence(0)
        for index, t in enumerate(time):
            ts.setTime(index + 1, t),

        # Set the finite element coordinate field for the nodes to use
        node_template.defineField(coordinate_field)
        node_template.defineField(self._string_field)
        node_template.setTimesequence(coordinate_field, ts)
        fieldcache = fieldmodule.createFieldcache()

        for label in self._labels:
            node_coordinates = self._trc_data[label]
            node = nodeset.createNode(-1, node_template)
            self._nodes.append(node)
            # Set the node coordinates, first set the field cache to use the current node
            fieldcache.setNode(node)
            for index, t in enumerate(time):
                fieldcache.setTime(t)
                # Pass in floats as an array
                coordinate_field.assignReal(fieldcache, node_coordinates[index])
                self._string_field.assignString(fieldcache, label)

        fieldmodule.endChange()
