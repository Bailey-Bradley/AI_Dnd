import pygame

class GameObject:

    def __init__(self):
        self.name = ""
        self.event_bus = None
        self.layer_query = None
        self.hierarchy = None

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