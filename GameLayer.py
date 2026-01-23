from GameObject import GameObject
import pygame
class LayerQuery:
    
    def __init__(self, objects):
        self.objects = objects

    def findObject(self, name):
        for object in self.objects:
            if object.name == name:
                return object

        return None

class GameLayer:
    def __init__(self):
        self.objects: list[GameObject] = []
        self.renderer = None
        self.event_busses = None
        self.layer_query: LayerQuery = LayerQuery(self.objects)

    def addObject(self, game_object: GameObject):
        self.objects.append(game_object)

        game_object.layer_query = self.layer_query
        game_object.onConnect()

    def removeObject(self, game_object: GameObject):
        self.objects.remove(game_object)

        game_object.onDisconnect()

    def giveEvents(self, events: list[pygame.event.Event]):
        pass

    def update(self):
        for game_object in self.objects:
            game_object.update()

    def render(self, surface):
        pass