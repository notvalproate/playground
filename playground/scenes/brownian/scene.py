import pygame
import pymunk
from typing import override

from playground.engine import Scene, Window, PhysicsObject

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
        self.line_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

        self.ball = PhysicsObject()

    @override
    def start(self) -> None:
        self.window.set_caption("Brownian Motion Sim")

        self.physics.set_gravity((0, 0))

        self.ball.body = pymunk.Body()
        self.ball.body.position = 0, 0
        
        self.ball.poly = pymunk.Circle(self.ball.body, 0.5)
        self.ball.poly.mass = 10

        self.physics.add_object(self.ball)

    @override
    def update(self) -> None: 
        self.apply_drag(self.ball.body)

        if self.pressed_keys[pygame.K_w]:
            self.ball.body.apply_force_at_local_point((0, 500))
        if self.pressed_keys[pygame.K_s]:
            self.ball.body.apply_force_at_local_point((0, -500))
        if self.pressed_keys[pygame.K_d]:
            self.ball.body.apply_force_at_local_point((500, 0))
        if self.pressed_keys[pygame.K_a]:
            self.ball.body.apply_force_at_local_point((-500, 0))   

        self.prev_position.x = self.position.x
        self.prev_position.y = self.position.y
        self.position.x = self.ball.body.position.x
        self.position.y = self.ball.body.position.y

    def apply_drag(self, body) -> None:
        v_len = body.velocity.length
        if v_len == 0:
            return
        
        drag_coefficient = 10
        drag_force_magnitude = drag_coefficient * v_len**2
        
        drag_force = -body.velocity.normalized() * drag_force_magnitude
        body.apply_force_at_local_point(drag_force, (0, 0))

    @override
    def draw(self) -> None:
        prev_surface = self.renderer.get_active_surface()
        self.renderer.set_active_surface(self.line_surface)

        self.renderer.draw_line_world(self.prev_position, self.position, 0.01, (0, 255, 0))

        self.renderer.set_active_surface(prev_surface)

        self.renderer.clear_color = (0, 0, 0)
        self.renderer.clear()
        self.renderer.draw_circle_fill(pygame.Vector2(self.ball.body.position.x, self.ball.body.position.y), 0.5, (0, 0, 255))
        self.renderer.blit_surface_world(self.line_surface)

        self.renderer.swap_display_buffers()

    @override
    def quit(self) -> None:
        print(f"Max X: {self.max_x} | Max Y: {self.max_y}")