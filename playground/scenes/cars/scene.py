import pygame
from typing import override

from playground.engine.scene import Scene
from playground.engine.window import Window
from playground.engine.rendering import Sprite

class CarsScene(Scene):
    position: pygame.Vector2
    delta: float
    sf25: Sprite
    welcome: str
    config: dict

    def __init__(self, window: Window):
        do_physics = False
        super().__init__(window, do_physics)

        self.position = pygame.Vector2(0, 0)
        self.delta = 0.05
        self.config = self.assets.load_config("config", "config.yaml")

        self.sf25 = self.assets.load_sprite("sf25", self.config["cars"]["sf25_path"])
        self.welcome = self.config["cars"]["welcome_text"]

    @override
    def update(self) -> None:
        self.position.x += self.delta

        if self.position.x >= 2 or self.position.x <= -2:
            self.delta *= -1

    @override
    def draw(self) -> None:
        self.renderer.clear()
        self.renderer.draw_circle_fill(self.position, 1.0)
        self.renderer.draw_text_world(
            self.welcome,
            pygame.Vector2(0.0, 2.5),
        )
        self.renderer.draw_sprite(self.sf25)
        self.renderer.swap_display_buffers()
