from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QFileDialog
import os

class LayerHandler:
    def __init__(self) -> None:
        self.instance = QgsProject.instance()
        self.jaltol_cols = ('State_N', 'Dist_N', 'SubDist_N', 'VCT_N')
    
    def get_layers(self, dropdown):
        layers = self.instance.layerTreeRoot().children()
        dropdown.clear()
        dropdown.addItems([layer.name() for layer in layers])
    
    def browse_input_shp(self):
        filepath, _ = QFileDialog.getOpenFileName(
            None, "Select shape file ","", '*.shp')
        if filepath:
            filename = os.path.splitext(os.path.basename(filepath))
            layer = QgsVectorLayer(filepath, filename[0], "ogr")
            self.instance.addMapLayer(layer)
    
    def check_layer(self, lyr_name):
        layers = QgsProject.instance().mapLayers().items()
        if layer := tuple(filter(lambda x: x[1].name() == lyr_name, layers)):
            field_names = layer[0][1].fields().names()
            return (all((name in field_names for name in self.jaltol_cols)))
        return False