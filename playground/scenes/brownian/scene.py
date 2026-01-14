import pygame
import pymunk
import math
from typing import override

from playground.engine import Scene, Window, PhysicsObject

import random

class BrownianScene(Scene):
    position: pygame.Vector2
    prev_position: pygame.Vector2
    delta: float
    max_x: float
    max_y: float
    line_surface: pygame.Surface

    ball: PhysicsObject

    def __init__(self, window: Window):
        do_physics = True
        super().__init__(window, do_physics)

        self.position = pygame.Vector2(0, 0)
        self.prev_position = pygame.Vector2(0, 0)
        self.delta = 0.05
        self.max_x = 0
        self.max_y = 0
        self.line_surface = pygame.Surface((800, 800), pygame.SRCALPHA)

        self.ball = PhysicsObject()

    @override
    def start(self) -> None:
        self.window.set_caption("Brownian Motion Sim")

        self.ball.body = pymunk.Body()
        self.ball.body.position = 0, 0
        
        self.ball.poly = pymunk.Circle(self.ball.body, 0.5)
        self.ball.poly.mass = 10

        self.physics.add_object(self.ball)

    @override
    def update(self) -> None: 
        self.prev_position.x = self.position.x
        self.prev_position.y = self.position.y

        random_dir = random.random() * 2 * math.pi
        random_amt = random.random()
        self.position.x += math.sin(random_dir) * self.delta * random_amt
        self.position.y += math.cos(random_dir) * self.delta * random_amt

        if abs(self.position.x) > self.max_x:
            self.max_x = abs(self.position.x)

        if abs(self.position.y) > self.max_y:
            self.max_y = abs(self.position.y)

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.window.toggle_fullscreen()

    @override
    def draw(self) -> None:
        prev_surface = self.renderer.get_active_surface()
        self.renderer.set_active_surface(self.line_surface)

        self.renderer.draw_line_world(self.prev_position, self.position, 0.01, (0, 255, 0))

        self.renderer.set_active_surface(prev_surface)

        self.renderer.clear_color = (0, 0, 0)
        self.renderer.clear()
        self.renderer.draw_circle_fill(self.position, 1.0)
        self.renderer.blit_surface_world(self.line_surface)

        self.renderer.draw_circle_fill(pygame.Vector2(self.ball.body.position[0], self.ball.body.position[1]), 0.5, (0, 0, 255))

        self.renderer.swap_display_buffers()

    @override
    def quit(self) -> None:
        print(f"Max X: {self.max_x} | Max Y: {self.max_y}")