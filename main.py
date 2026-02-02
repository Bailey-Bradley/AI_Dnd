import pygame
import math
from engine.GameObject import GameObject
from engine.GameLayer import GameLayer
from engine.GameLayerStack import GameLayerStack
from engine.Renderer import ERenderLayer
import random
from engine.LayerManager import LayerManager
from engine.Events import EventBus, UserEvent
from engine.Audio import AudioManager, AudioPlayer
from engine.Resources import ResourceManager
from pathlib import Path


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
        background = self.layer_query.findObject("Background")
        self.hierarchy.addChild(background, self)

    def update(self):
        self.ticker += 1

        self.guy = pygame.transform.scale(self.guy, tuple(x * (math.sin(self.ticker * 0.1) + 2) for x in self.size))

    def nudge(self, event):
        match event.unicode:
            case 'd':
                self.x += 10
                background = self.hierarchy.getParent(self)
                background.surface.fill((0,random.randrange(100),0))
            case 'a':
                self.x -= 10
            case 'w':
                self.y -= 10
            case 's':
                self.y += 10
            case 'u':
                LayerManager.saveLayer()
            case 'o':
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
pygame.mixer.init()

main_window = pygame.display.set_mode((1000,750), pygame.RESIZABLE)
clocky = pygame.time.Clock()
global_bus = EventBus()
AudioManager.init(global_bus)
ResourceManager.init(Path(__file__).parent)

layer_stack = GameLayerStack(main_window)
layer_manager = LayerManager(layer_stack)

layer1 = GameLayer()

obj1 = DefaultObj()
obj2 = Background(main_window.get_size(), (0,2,0))

layer1.addObject(obj2, ERenderLayer.BACKGROUND)
layer1.addObject(obj1)

layer_stack.addLayer(layer1)

audio_player = AudioPlayer()

audio_player.playMusic(["yell", "boing"])

running = True
while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'p':
                audio_player.playSound("yell")

        global_bus.emit(event.type, event)

    layer_stack.update(events)

    clocky.tick(40)

    pygame.display.flip()