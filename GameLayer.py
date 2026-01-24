from GameObject import GameObject
from Hierarchy import ObjectHierarchy
import Events
import pygame
import Serialize


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
        self.renderer = None
        self.event_busses: list[Events.EventBus] = [Events.EventBus()]
        self.layer_query: LayerQuery = LayerQuery(self.objects)

    def addObject(self, game_object: GameObject):
        self.hierarchy.addObject(game_object)

        game_object.layer_query = self.layer_query
        game_object.event_bus = self.event_busses[-1]
        game_object.onConnect()

    def removeObject(self, game_object: GameObject):
        self.hierarchy.removeObject(game_object)

        game_object.onDisconnect()
        game_object.event_bus = None
        game_object.layer_query = None

    def giveEvents(self, events: list[pygame.event.Event]):
        pass

    def update(self):
        for game_object in self.hierarchy.getObjects():
            game_object.update()

    def render(self, surface):
        pass

    def onSerialize(self):
        for event_bus in self.event_busses:
            event_bus.onSerialize()

    def onDeserialize(self):

        for event_bus in self.event_busses:
            event_bus.onDeserialize()

        for obj in self.hierarchy.getObjects():
            obj.onDeserialize()