'''
MAP Client Plugin Step
'''
import os

import json
from PySide2 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.mocapdataviewerstep.configuredialog import ConfigureDialog
from mapclientplugins.mocapdataviewerstep.mocapviewer import MOCAPViewer


class MOCAPDataViewerStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(MOCAPDataViewerStep, self).__init__('MOCAP Data Viewer', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'General'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/mocapdataviewerstep/images/mocapdataviewericon.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#trcdata'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#trcdata'))
        self._config = {}
        self._config['identifier'] = ''
        self._trc_data = None
        self._view = None

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        if not self._view:
            self._view = MOCAPViewer(self._trc_data)
            self._view._ui.pushButtonDone.clicked.connect(self._doneExecution)

        #         self._setCurrentUndoRedoStack(self._model.getUndoRedoStack())
        self._setCurrentWidget(self._view)

    #         self._doneExecution()

    def _viewerClosed(self):
        self._trc_data = self._view.getTRCData()
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        self._trc_data = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#trcdata

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        # http://physiomeproject.org/workflow/1.0/rdf-schema#trcdata
        return self._trc_data

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
