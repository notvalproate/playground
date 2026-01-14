import pygame
from typing import List

from playground.engine.rendering import Renderer 
from playground.engine.camera import Camera
from playground.engine.window import Window
from playground.engine.physics import Physics

class Scene:
    window: Window
    main_camera: Camera
    renderer: Renderer
    framerate: int
    events: List[pygame.event.Event]
    physics: Physics
    frametime: int

    def __init__(self, window: Window, do_physics: bool) -> None:
        self.window = Window()
        self.main_camera = Camera()
        self.renderer = Renderer(window.surface, self.main_camera)
        self.framerate = 60
        self.events = []

        self.physics = Physics() if do_physics else None

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