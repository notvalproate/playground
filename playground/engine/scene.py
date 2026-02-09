import pygame
import sys
from typing import List
from pathlib import Path

from playground.engine.rendering import Renderer 
from playground.engine.camera import Camera
from playground.engine.window import Window
from playground.engine.physics import Physics
from playground.engine.assets import AssetManager

class Scene:
    window: Window
    main_camera: Camera
    renderer: Renderer
    assets: AssetManager
    framerate: int
    events: List[pygame.event.Event]
    pressed_keys: List[int]
    physics: Physics
    frametime: int

    def __init__(self, window: Window, do_physics: bool) -> None:
        self.window = Window()
        self.main_camera = Camera()
        self.renderer = Renderer(window.surface, self.main_camera)

        self.framerate = 60
        self.events = []
        self.pressed_keys = []

        self.physics = Physics() if do_physics else None
        
        module = sys.modules[self.__module__]
        scene_file = Path(module.__file__).resolve()
        self.assets = AssetManager(scene_file.parent / "assets")

    def start(self) -> None:
        pass

    def before_update(self) -> None:
        pass

    def update(self) -> None:
        pass

    def after_update(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def quit(self) -> None:
        pass