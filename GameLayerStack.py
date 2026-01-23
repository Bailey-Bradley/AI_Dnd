from GameLayer import GameLayer
import pygame


class GameLayerStack:
    def __init__(self, main_window):
        self.layers: list[GameLayer] = []

        self.main_window = main_window

    def addLayer(self, layer: GameLayer):
        self.layers.append(layer)

    def removeLayer(self, layer: GameLayer):
        self.layers.remove(layer)

    def popLayer(self):
        if len(self.layers) > 0:
            self.removeLayer(self.layers[-1])

    def update(self):

        if len(self.layers) > 0:
            self.layers[-1].update()