import pymunk
from typing import List, Tuple


class PhysicsObject:
    body: pymunk.Body
    poly: pymunk.Poly
    
    def __init__(self) -> None:
        self.body = None
        self.poly = None


class Physics:
    space: pymunk.Space
    objects: List[PhysicsObject]
    debug_draw: bool

    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = 0, -9.81
        self.objects = []
        self.debug_draw = False

    def set_gravity(self, gravity: Tuple[float, float]) -> None:
        self.space.gravity = gravity

    def add_object(self, object: PhysicsObject) -> None:
        self.objects.append(object)
        self.space.add(object.body, object.poly)

    def step(self, time: float) -> None:
        self.space.step(time)
