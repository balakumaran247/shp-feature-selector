from qgis.core import QgsProject, QgsVectorLayer, QgsExpression, QgsFeatureRequest
from qgis.PyQt.QtWidgets import QFileDialog
import os
from .gui.filter_selector import Ui_Form as filter_main_widget


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

    def get_col_names(self, layer):
        return layer.fields().names()

    def check_layer(self, layer):
        field_names = self.get_col_names(layer)
        return (all((name in field_names for name in self.jaltol_cols)))

    def get_layer(self, lyr_name):
        if layers:= self.instance.mapLayersByName(lyr_name):
            return layers[0]

    def get_unique_values(self, layer, col_name):
        idx = layer.fields().indexOf(col_name)
        return sorted(map(lambda x: str(x), filter(lambda y: isinstance(y, (str, int, float)), layer.uniqueValues(idx))))

    def get_state_list(self, layer):
        return self.get_unique_values(layer, self.jaltol_cols[0])

    def get_dist_list(self, layer, state):
        stateFilter = self._get_filter_exp((self.jaltol_cols[0], state))
        return self._extract_info(stateFilter, layer, self.jaltol_cols[1])

    def get_block_list(self, layer, state, dist):
        vlayerFilter = self._get_filter_exp(
            (self.jaltol_cols[0], state),
            (self.jaltol_cols[1], dist)
        )
        return self._extract_info(vlayerFilter, layer, self.jaltol_cols[2])

    def get_village_list(self, layer, state, dist, block):
        vlayerFilter = self._get_filter_exp(
            (self.jaltol_cols[0], state),
            (self.jaltol_cols[1], dist),
            (self.jaltol_cols[2], block)
        )
        return self._extract_info(vlayerFilter, layer, self.jaltol_cols[3])

    def _extract_info(self, vlayerFilter, layer, col_name):
        expr = QgsExpression(vlayerFilter)
        col_feas = layer.getFeatures(QgsFeatureRequest(expr))
        li = [fea[col_name] for fea in col_feas if fea[col_name]]
        return sorted(set(filter(lambda x: isinstance(x, str), li)))

    def _get_filter_exp(self, *args):
        return ' and '.join(map(lambda x: f"\"{x[0]}\"='{x[1]}'", args))

class AddFilters(LayerHandler):
    def __init__(self, fields, expr_list, layout, layer, Form) -> None:
        self.fields = fields
        self.expr_list = expr_list
        self.layout = layout
        self.layer = layer
        self.Form = Form
        self.create_dd()
        self.populate_filter_main()
    
    def create_dd(self):
        self.add_widget = filter_main_widget()
        self.add_widget.setupUi(self.Form)
        self.layout.addWidget(self.add_widget.widget)
        self.add_widget.heading_selector.currentIndexChanged.connect(lambda: self.populate_value_dd())
        self.add_widget.value_selector.currentIndexChanged.connect(lambda: self.child_item())
    
    def populate_filter_main(self):
        self.add_widget.heading_selector.blockSignals(True)
        self.populate_dd(self.add_widget.heading_selector, self.fields)
        self.add_widget.heading_selector.blockSignals(False)
    
    def populate_value_dd(self):
        self.selected_field = self.add_widget.heading_selector.currentText()
        print(self.selected_field)
        if self.selected_field != 'select':
            vlayerFilter = self._get_filter_exp(*self.expr_list)
            dd_values = ['select'] + list(self._extract_info(vlayerFilter, self.layer, self.selected_field))
            self.add_widget.value_selector.blockSignals(True)
            self.populate_dd(self.add_widget.value_selector, dd_values)
            self.add_widget.value_selector.blockSignals(False)
    
    def child_item(self):
        self.selected_value = self.add_widget.value_selector.currentText()
        new_fields = self.fields.copy()
        new_fields.remove(self.selected_field)
        new_expr_list = self.expr_list.copy()
        new_expr_list.append((self.selected_field, self.selected_value))
        print(new_fields)
        print(new_expr_list)
