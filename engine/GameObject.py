import pygame
from engine import Events
from engine.Serialize import Serializable
from engine.Hierarchy import ObjectHierarchy

class GameObject(Serializable):

    def __init__(self):
        self.name = ""
        self.event_bus: Events.EventBus = None
        self.layer_query = None
        self.hierarchy: ObjectHierarchy = None

        self.parent: GameObject = None
        self.children: list[GameObject] = []

        self.components = []

    def onConnect(self):
        pass

    def onDisconnect(self):
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass