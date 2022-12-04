from qgis.core import QgsProject, QgsVectorLayer, QgsExpression, QgsFeatureRequest
from qgis.PyQt.QtWidgets import QFileDialog
import os


class LayerHandler:
    def __init__(self) -> None:
        self.instance = QgsProject.instance()
        self.jaltol_cols = ('State_N', 'Dist_N', 'SubDist_N', 'VCT_N')

    def populate_dd(self, dropdown, ilist):
        dropdown.clear()
        if ilist:
            dropdown.addItems(ilist)

    def layers_dd(self, dropdown):
        layers = self.instance.layerTreeRoot().children()
        self.populate_dd(dropdown, [layer.name() for layer in layers])

    def browse_input_shp(self):
        filepath, _ = QFileDialog.getOpenFileName(
            None, "Select shape file ", "", '*.shp')
        if filepath:
            filename = os.path.splitext(os.path.basename(filepath))
            layer = QgsVectorLayer(filepath, filename[0], "ogr")
            self.instance.addMapLayer(layer)

    def check_layer(self, layer):
        field_names = layer.fields().names()
        return (all((name in field_names for name in self.jaltol_cols)))

    def get_layer(self, lyr_name):
        if layers:
            = self.instance.mapLayersByName(lyr_name):
            return layers[0]

    def get_state_list(self, layer):
        idx = layer.fields().indexOf(self.jaltol_cols[0])
        return sorted(filter(lambda x: isinstance(x, str), layer.uniqueValues(idx)))

    def get_dist_list(self, layer, state):
        stateFilter = f"\"{self.jaltol_cols[0]}\"='{state}'"
        return self._extract_info(stateFilter, layer, self.jaltol_cols[1])

    def get_block_list(self, layer, state, dist):
        stateFilter = f"\"{self.jaltol_cols[0]}\"='{state}'"
        distFilter = f"\"{self.jaltol_cols[1]}\"='{dist}'"
        vlayerFilter = f'{stateFilter} and {distFilter}'
        return self._extract_info(vlayerFilter, layer, self.jaltol_cols[2])

    def get_village_list(self, layer, state, dist, block):
        stateFilter = f"\"{self.jaltol_cols[0]}\"='{state}'"
        distFilter = f"\"{self.jaltol_cols[1]}\"='{dist}'"
        blockFilter = f"\"{self.jaltol_cols[2]}\"='{block}'"
        vlayerFilter = f'{stateFilter} and {distFilter} and {blockFilter}'
        return self._extract_info(vlayerFilter, layer, self.jaltol_cols[3])

    def _extract_info(self, vlayerFilter, layer, col_name):
        expr = QgsExpression(vlayerFilter)
        stateFeas = layer.getFeatures(QgsFeatureRequest(expr))
        li = [fea[col_name] for fea in stateFeas if fea[col_name]]
        return sorted(set(filter(lambda x: isinstance(x, str), li)))
