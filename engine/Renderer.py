from engine.GameObject import GameObject
from enum import Enum


class ERenderLayer(Enum):
    BACKGROUND = 0
    FOREGROUND = 1
    FOREGROUND_OVERLAY = 2
    UI = 3
    UI_OVERLAY = 4


class Renderer:
    def __init__(self):
        self.layers: dict[str, list[GameObject]] = {}

    def render(self, surface) -> None:
        for layer_type in ERenderLayer:
            layer = self.layers.get(layer_type.name)
            if layer is not None:
                for obj in layer:
                    obj.render(surface)

    def addToLayer(self, gameobj: GameObject, layer: ERenderLayer) -> None:

        render_layer = self.layers.get(layer.name)

        if render_layer is not None:
            render_layer.append(gameobj)
        else:
            self.layers[layer.name] = [gameobj]

    def removeFromLayer(self, gameobj: GameObject) -> None:
        for layer in self.layers.values():
            layer.remove(gameobj)