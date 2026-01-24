from engine.Renderer import Renderer
from engine.Renderer import ERenderLayer
from engine.GameObject import GameObject
from engine.Hierarchy import ObjectHierarchy
from engine import Events
import pygame
from engine import Serialize


class LayerQuery:
    
    def __init__(self, objects):
        self.objects = objects

    def findObject(self, name):
        for object in self.objects:
            if object.name == name:
                return object

        return None

class GameLayer(Serialize.Serializable):
    def __init__(self):
        self.hierarchy: ObjectHierarchy = ObjectHierarchy()
        self.renderer = Renderer()
        self.event_busses: list[Events.EventBus] = [Events.EventBus()]
        self.layer_query: LayerQuery = LayerQuery(self.hierarchy.getObjects())

    def addObject(self, game_object: GameObject, render_layer: ERenderLayer = ERenderLayer.FOREGROUND):
        self.hierarchy.addObject(game_object)
        self.renderer.addToLayer(game_object, render_layer)

        game_object.layer_query = self.layer_query
        game_object.event_bus = self.event_busses[-1]
        game_object.hierarchy = self.hierarchy
        game_object.onConnect()

    def removeObject(self, game_object: GameObject):
        self.hierarchy.removeObject(game_object)
        self.renderer.removeFromLayer(game_object)

        game_object.onDisconnect()
        game_object.event_bus = None
        game_object.layer_query = None
        game_object.hierarchy = None

    def _processInput(self, input_events: list[pygame.event.Event]):
        for event in input_events:
            self.event_busses[-1].emit(event.type, event)

    def giveEvents(self, events: list[pygame.event.Event]):

        input_events = []

        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                input_events.append(event)

        self._processInput(input_events)

    def update(self):
        for game_object in self.hierarchy.getObjects():
            game_object.update()

    def render(self, surface):
        self.renderer.render(surface)

    def onSerialize(self):
        for event_bus in self.event_busses:
            event_bus.onSerialize()

    def onDeserialize(self):

        for event_bus in self.event_busses:
            event_bus.onDeserialize()

        for obj in self.hierarchy.getObjects():
            obj.onDeserialize()