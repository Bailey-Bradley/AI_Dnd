import Serialize
from GameLayerStack import GameLayerStack
from GameLayer import GameLayer
import Log


class LayerManager:

    _instance = None

    def __new__(cls, layer_stack: GameLayerStack):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance._layer_stack = layer_stack
        else:
            return cls._instance

    def replaceLayer(layer_name):
        layer = Serialize.load(layer_name)

        if layer is not None:
            LayerManager._instance._layer_stack.popLayer()
            LayerManager._instance._layer_stack.addLayer(layer)

    def saveLayer():
        top_layer = LayerManager._instance._layer_stack.layers[-1]
        Serialize.save(top_layer, "quicksave")