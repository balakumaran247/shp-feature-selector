from . import feature_selector_ui
from qgis.PyQt.QtWidgets import QAction


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
        self.dlg = feature_selector_ui.MyDockWidget(
            parent=self.iface.mainWindow())
        self.dlg.show()
