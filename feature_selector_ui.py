from qgis.PyQt import QtCore, QtGui, QtWidgets
from .gui.home_widget import Ui_Form as home_widget
from .gui.input_layer_selector import Ui_input_selector_form as lyr_selector
from .gui.selector_panel import Ui_Form as selector_widget
from .gui.filter_selector import Ui_Form as filter_main_widget
from .gui.main_window import Ui_MainWindow
from .feature_selector_core import LayerHandler, AddFilters


class MyDockWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.verticalLayout_2.addWidget(self.contents())
        self.layers_class = LayerHandler()
        self.get_input_layers()

    def contents(self):
        self.Form = QtWidgets.QWidget()
        self.home_win()
        self.layer_panel()
        self.selector_panel()
        self.filter_panel()
        return self.Form

    def home_win(self):
        self.home_ui = home_widget()
        self.home_ui.setupUi(self.Form)
        self.home_ui.stackedWidget.setCurrentIndex(0)

    def layer_panel(self):
        self.layer_ui = lyr_selector()
        self.layer_ui.setupUi(self.Form)
        self.home_ui.main_input_layout.addWidget(self.layer_ui.layoutWidget)
        self.layer_ui.browse_button.clicked.connect(self.browse_shp)
        self.layer_ui.input_layer_dd.currentIndexChanged.connect(
            self.choose_page)

    def selector_panel(self):
        self.selector_ui = selector_widget()
        self.selector_ui.setupUi(self.Form)
        self.home_ui.selector_placeholder.setLayout(
            self.selector_ui.verticalLayout_2)
        self.selector_ui.state_dd.currentIndexChanged.connect(
            self.populate_dist)
        self.selector_ui.district_dd.currentIndexChanged.connect(
            self.populate_block)
        self.selector_ui.block_dd.currentIndexChanged.connect(
            self.populate_village)
        self.selector_ui.village_dd.currentIndexChanged.connect(
            self.select_feature)

    def filter_panel(self):
        self.add_filter = None
        self.filter_main = filter_main_widget()
        self.filter_main.setupUi(self.Form)
        self.home_ui.filter_placeholder_layout.addWidget(
            self.filter_main.widget)
        self.filter_main.heading_selector.currentIndexChanged.connect(
            self.populate_fm_value)
        self.filter_main.value_selector.currentIndexChanged.connect(
            self.add_fa_dd)
        self.spacerItem = QtWidgets.QSpacerItem(
            20, 182, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.home_ui.filter_placeholder_layout.addItem(self.spacerItem)

    def get_input_layers(self):
        self.layers_class.layers_dd(self.layer_ui.input_layer_dd)

    def browse_shp(self):
        self.layers_class.browse_input_shp()
        self.get_input_layers()

    def choose_page(self):
        layer_name = self.layer_ui.input_layer_dd.currentText()
        self.layer = self.layers_class.get_layer(layer_name)
        if self.layer and self.layers_class.check_layer(self.layer):
            self.home_ui.stackedWidget.setCurrentWidget(self.home_ui.page)
            self.populate_state()
        else:
            self.home_ui.stackedWidget.setCurrentWidget(self.home_ui.page_2)
            self.populate_filter_main()

    def populate_state(self):
        slist = self.layers_class.get_state_list(self.layer)
        self.layers_class.populate_dd(self.selector_ui.state_dd, slist)

    def populate_dist(self):
        self.state = self.selector_ui.state_dd.currentText()
        dlist = self.layers_class.get_dist_list(self.layer, self.state)
        self.layers_class.populate_dd(self.selector_ui.district_dd, dlist)

    def populate_block(self):
        self.dist = self.selector_ui.district_dd.currentText()
        blist = self.layers_class.get_block_list(
            self.layer, self.state, self.dist)
        self.layers_class.populate_dd(self.selector_ui.block_dd, blist)

    def populate_village(self):
        self.block = self.selector_ui.block_dd.currentText()
        vlist = self.layers_class.get_village_list(
            self.layer, self.state, self.dist, self.block)
        self.layers_class.populate_dd(self.selector_ui.village_dd, vlist)

    def select_feature(self):
        self.village = self.selector_ui.village_dd.currentText()
        self.layers_class.select_village(
            self.state, self.dist, self.block, self.village, self.layer)

    def populate_filter_main(self):
        self.filtered_col = []
        if self.layer:
            self.field_cols = [
                'select'] + sorted(set(self.layers_class.get_col_names(self.layer)))
            self.filter_main.heading_selector.blockSignals(True)
            self.layers_class.populate_dd(
                self.filter_main.heading_selector, self.field_cols)
            self.filter_main.heading_selector.blockSignals(False)

    def populate_fm_value(self):
        if self.add_filter:
            self.add_filter.del_child()
            self.add_filter.add_widget.widget.setParent(None)
        self.main_heading_selected = self.filter_main.heading_selector.currentText()
        value_list = [
            'select'] + self.layers_class.get_unique_values(self.layer, self.main_heading_selected)
        self.filter_main.value_selector.blockSignals(True)
        self.layers_class.populate_dd(
            self.filter_main.value_selector, value_list)
        self.filter_main.value_selector.blockSignals(False)

    def add_fa_dd(self):
        main_value_selected = self.filter_main.value_selector.currentText()
        if main_value_selected != 'select':
            new_fields = self.field_cols.copy()
            new_fields.remove(self.main_heading_selected)
            self.add_filter = AddFilters(
                new_fields,
                [(self.main_heading_selected, main_value_selected)],
                self.home_ui,
                self.layer,
                self.Form,
                self.spacerItem)
