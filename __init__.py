from .feature_selector import FeatureSelectorPlugin

def classFactory(iface):
    return FeatureSelectorPlugin(iface)