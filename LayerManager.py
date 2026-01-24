import Serialize
from GameLayerStack import GameLayerStack
from GameLayer import GameLayer
import Log


class LayerManager:

    _Instance = None

    def __init__(self, layer_stack: GameLayerStack):
        if LayerManager._Instance is not None:
            return LayerManager._Instance
        else:
            self._layer_stack = layer_stack
            LayerManager._Instance = self

    def replaceLayer(layer_name):
        layer = Serialize.load(layer_name)

        if layer is not None:
            LayerManager._Instance._layer_stack.popLayer()
            LayerManager._Instance._layer_stack.addLayer(layer)

    def saveLayer():
        top_layer = LayerManager._Instance._layer_stack.layers[-1]
        Serialize.save(top_layer, "quicksave")