import pygame
from typing import List

from playground.engine.rendering import Renderer 
from playground.engine.camera import Camera
from playground.engine.window import Window

class Scene:
    window: Window
    main_camera: Camera
    renderer: Renderer
    framerate: int
    events: List[pygame.event.Event]

    def __init__(self, window: Window) -> None:
        self.window = Window()
        self.main_camera = Camera()
        self.renderer = Renderer(window.surface, self.main_camera)
        self.framerate = 60
        self.events = []

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