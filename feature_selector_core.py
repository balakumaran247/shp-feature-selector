from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QFileDialog
import os

class LayerHandler:
    
    def get_layers(self, dropdown):
        layers = QgsProject.instance().layerTreeRoot().children()
        dropdown.clear()
        dropdown.addItems([layer.name() for layer in layers])
    
    def browse_input_shp(self):
        filepath, _ = QFileDialog.getOpenFileName(
            None, "Select shape file ","", '*.shp')
        filename = os.path.splitext(os.path.basename(filepath))
        layer = QgsVectorLayer(filepath, filename[0], "ogr")
        QgsProject.instance().addMapLayer(layer)