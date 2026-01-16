import pygame
import pymunk
from typing import override, List, Tuple

from playground.engine import Scene, Window, PhysicsObject

class Wall:
    obj: PhysicsObject
    center: pygame.Vector2
    width: float
    height: float

    def __init__(self) -> None:
        self.obj = PhysicsObject()
        self.center = pygame.Vector2()
        self.width = 1
        self.height = 1

class BrownianScene(Scene):
    position: pygame.Vector2
    prev_position: pygame.Vector2
    delta: float
    max_x: float
    max_y: float
    line_surface: pygame.Surface

    ball: PhysicsObject
    walls: List[Wall]
    atoms: List[PhysicsObject]

    def __init__(self, window: Window):
        do_physics = True
        super().__init__(window, do_physics)

        self.position = pygame.Vector2(0, 0)
        self.prev_position = pygame.Vector2(0, 0)
        self.delta = 0.05
        self.max_x = 0
        self.max_y = 0
        self.line_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

        self.ball = None
        self.walls = []

    @override
    def start(self) -> None:
        self.window.set_caption("Brownian Motion Sim")

        self.physics.debug_draw = True
        self.physics.set_gravity((0, 0))

        # Creating Ball

        self.ball = self.create_ball((0, 0), 0.5, 10)
        self.physics.add_object(self.ball)

        # Creating Walls

        top_left = pygame.Vector2(-5, 3)
        width = 10
        height = 6
        wall_thickness = 0.3

        offset_y = top_left.y - (wall_thickness / 2)
        offset_x = top_left.x + (wall_thickness / 2)

        wall_top = self.create_wall(0, offset_y, width, wall_thickness)
        wall_bottom = self.create_wall(0, -offset_y, width, wall_thickness)
        wall_left = self.create_wall(offset_x, 0, wall_thickness, height)
        wall_right = self.create_wall(-offset_x, 0, wall_thickness, height)

        self.walls.append(wall_top)
        self.walls.append(wall_bottom)
        self.walls.append(wall_left)
        self.walls.append(wall_right)

        # Add all walls

        for wall in self.walls:
            self.physics.add_object(wall.obj)

    def create_ball(self, pos: Tuple[float, float], r: float, m: float) -> PhysicsObject:
        ball = PhysicsObject()
        ball.body = pymunk.Body()
        ball.body.position = pos
        
        ball.poly = pymunk.Circle(ball.body, r)
        ball.poly.mass = m
        ball.poly.elasticity = 1
        ball.poly.friction = 0

        return ball

    def create_wall(self, x, y, w, h) -> Wall:   
        wall = Wall()

        wall.obj.body = pymunk.Body()
        wall.obj.body.position = (x, y)
        wall.obj.body.body_type = pymunk.Body.STATIC

        wall.center = pygame.Vector2(wall.obj.body.position.x, wall.obj.body.position.y)
        wall.width = w
        wall.height = h

        wall.obj.poly = pymunk.Poly.create_box(wall.obj.body, (w, h))
        wall.obj.poly.elasticity = 1
        wall.obj.poly.friction = 0

        return wall


    @override
    def update(self) -> None: 
        # self.apply_drag(self.ball.body)

        if self.pressed_keys[pygame.K_w]:
            self.ball.body.apply_force_at_local_point((0, 200))
        if self.pressed_keys[pygame.K_s]:
            self.ball.body.apply_force_at_local_point((0, -200))
        if self.pressed_keys[pygame.K_d]:
            self.ball.body.apply_force_at_local_point((200, 0))
        if self.pressed_keys[pygame.K_a]:
            self.ball.body.apply_force_at_local_point((-200, 0))   

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

        for wall in self.walls:
            self.renderer.draw_rect_fill((wall.center.x, wall.center.y, wall.width, wall.height), 0, (204, 203, 122))

        self.renderer.blit_surface_world(self.line_surface)