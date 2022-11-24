import os
import sys
import inspect
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class FeatureSelectorPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('feature selector',
                              self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu('&feature selector', self.action)

    def unload(self):
        self.iface.removePluginMenu('&feature selector', self.action)
        del self.action

    def run(self):
        self.iface.messageBar().pushMessage('hello from feature selector plugin')
