"""Música de fundo opcional."""
import os
from pathlib import Path

MUSIC_FILE = Path(__file__).parent / "assets" / "buck.mp3"

def start(volume=0.4):
    if os.environ.get("POLIMEROS_FAST") == "1":
        return
    try:
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(str(MUSIC_FILE))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1)   # repete para sempre
    except Exception:
        pass  # sem pygame, sem arquivo ou sem placa de som

def stop():
    try:
        import pygame
        pygame.mixer.music.fadeout(1000)
    except Exception:
        pass
