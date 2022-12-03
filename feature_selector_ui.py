
from qgis.PyQt import QtCore, QtGui, QtWidgets
from .gui.home_widget import Ui_Form as home_widget
from .gui.input_layer_selector import Ui_input_selector_form as lyr_selector
from .gui.selector_panel import Ui_Form as selector_widget
from .gui.filter_selector import Ui_Form as filter_main_widget
from .gui.filter_selector_add import Ui_Form as filter_additional_widget
from .gui.main_window import Ui_MainWindow
from .feature_selector_core import LayerHandler


class MyDockWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.verticalLayout_2.addWidget(self.contents())
        self.layers_class = LayerHandler()
        self.get_input_layers()

    def contents(self):
        Form = QtWidgets.QWidget()
        home_ui = home_widget()
        home_ui.setupUi(Form)
        self.layer_ui = lyr_selector()
        self.layer_ui.setupUi(Form)
        home_ui.main_input_layout.addWidget(self.layer_ui.layoutWidget)
        self.layer_ui.browse_button.clicked.connect(self.browse_shp)
        selector_ui = selector_widget()
        selector_ui.setupUi(Form)
        home_ui.selector_placeholder.setLayout(selector_ui.verticalLayout_2)
        filter_main = filter_main_widget()
        filter_main.setupUi(Form)
        home_ui.filter_placeholder_layout.addWidget(filter_main.widget)
        home_ui.stackedWidget.setCurrentWidget(home_ui.page_2)
        spacerItem = QtWidgets.QSpacerItem(
            20, 182, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        home_ui.filter_placeholder_layout.addItem(spacerItem)
        for _ in range(4):
            home_ui.filter_placeholder_layout.removeItem(spacerItem)
            add_widget = filter_additional_widget()
            add_widget.setupUi(Form)
            home_ui.filter_placeholder_layout.addWidget(add_widget.widget)
            home_ui.filter_placeholder_layout.addItem(spacerItem)
        return Form
    
    def get_input_layers(self):
        self.layers_class.get_layers(self.layer_ui.input_layer_dd)
    
    def browse_shp(self):
        self.layers_class.browse_input_shp()
        self.get_input_layers()
