import pymunk
from typing import List


class PhysicsObject:
    body: pymunk.Body
    poly: pymunk.Poly
    
    def __init__(self) -> None:
        self.body = None
        self.poly = None


class Physics:
    space: pymunk.Space
    bodies: List[PhysicsObject]

    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = 0, -9.81
        self.bodies = []

    def add_object(self, object: PhysicsObject) -> None:
        self.space.add(object.body, object.poly)

    def step(self, time: float) -> None:
        self.space.step(time)
