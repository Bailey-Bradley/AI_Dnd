import pygame
from collections import deque
from engine.Resources import ResourceManager
from engine.Events import UserEvent, EventBus
from pathlib import Path

class AudioManager:

    music_queue: deque = deque()

    def init(event_bus: EventBus):
        event_bus.subscribe(UserEvent.SONG_ENDED.value, AudioManager.playQueued)

    def playSound(sound_name: str):
        with open(f"{ResourceManager.SOUND}/sounds/{sound_name}.mp3") as sound_file:

            if sound_file is not None:
                sound = pygame.mixer.Sound(sound_file)
                sound.play()
            else:
                pass
                # LOG a warning?

    def _loadMusic(music_name: str) -> bool:
        music_file = Path(f"{ResourceManager.SOUND}/music/{music_name}.mp3")

        if music_file.exists():
            pygame.mixer.music.load(music_file, "mp3")
            return True
        else:
            return False

    def playMusic(music_name: str, fade_duration: int = 0, loops: int = -1):

        musicLoaded = AudioManager._loadMusic(music_name)
        
        if musicLoaded is True:
            pygame.mixer.music.play(fade_ms=fade_duration, loops=loops)
            pygame.mixer.music.set_endevent()

    def stopMusic():
        pass

    def playSet(music_list: list[str]):
        AudioManager.music_queue = deque(music_list)
        pygame.mixer.music.set_endevent(UserEvent.SONG_ENDED.value)
        AudioManager.playQueued(None)

    def playQueued(event):
        for _ in range(len(AudioManager.music_queue)):
            next_song = AudioManager.music_queue.popleft()
            AudioManager.music_queue.append(next_song)

            musicLoaded = AudioManager._loadMusic(next_song)

            if musicLoaded is True:
                pygame.mixer.music.play()
                break

        return

class AudioPlayer:
    def __init__(self):
        pass

    def playSound(self, sound_name: str):
        AudioManager.playSound(sound_name)

    def playMusic(self, music_list: str | list[str], fade_duration: int = 0, loops: int = -1):
        if type(music_list) is list:
            AudioManager.playSet(music_list)
        else:
            AudioManager.playMusic(music_list, fade_duration, loops)

    def stopMusic(self, fade_duration: int = 0):
        pass