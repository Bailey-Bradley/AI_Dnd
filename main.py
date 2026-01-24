import pygame
import math
from engine.GameObject import GameObject
from engine.GameLayer import GameLayer
from engine.GameLayerStack import GameLayerStack
from engine.Renderer import ERenderLayer
import random
import engine.Serialize
from engine.LayerManager import LayerManager

class DefaultObj(GameObject):

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.size = (100,100)
        self.guy = pygame.Surface(self.size)
        self.guy.fill((0,20,0))
        self.ticker = 0

    def onConnect(self):
        self.event_bus.subscribe(pygame.KEYDOWN, self.nudge)

    def update(self):
        self.ticker += 1

        self.guy = pygame.transform.scale(self.guy, tuple(x * (math.sin(self.ticker * 0.1) + 2) for x in self.size))

    def nudge(self, event):
        if event.unicode == 'd':
            self.x += 10
            background = self.layer_query.findObject("Background")
            if background is None:
                print("not found")
            else:
                background.surface.fill((0,random.randrange(100),0))
        elif event.unicode == 'a':
            self.x -= 10
        elif event.unicode == 'w':
            self.y -= 10
        elif event.unicode == 's':
            self.y += 10
        elif event.unicode == 'u':
            LayerManager.saveLayer()
        elif event.unicode == 'o':
            LayerManager.replaceLayer("quicksave")

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.guy, (self.x, self.y))

    def postDeserialize(self):
        self.guy = pygame.Surface(self.size)
        self.guy.fill((0,20,0))


class Background(GameObject):
    def __init__(self, size: tuple[int, int], color: tuple[int, int, int]):
        super().__init__()
        self.init_params = (size, color)
        self.name = "Background"
        self.surface = pygame.Surface(size)
        self.surface.fill(color)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, (0,0))

    def postDeserialize(self):

        size, color = self.init_params

        self.surface = pygame.Surface(size)
        self.surface.fill(color)


pygame.init()

main_window = pygame.display.set_mode((1000,750), pygame.RESIZABLE)
clocky = pygame.time.Clock()

layer1 = GameLayer()

obj1 = DefaultObj()
obj2 = Background(main_window.get_size(), (0,2,0))

layer1.addObject(obj1)
layer1.addObject(obj2, ERenderLayer.BACKGROUND)

layer_stack = GameLayerStack(main_window)
layer_stack.addLayer(layer1)

LayerManager(layer_stack)

running = True
while running:

    layer_stack.update()

    clocky.tick(40)

    pygame.display.flip()
    