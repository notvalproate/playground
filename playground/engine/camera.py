import pygame
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class CameraFollowable(ABC):
    @abstractmethod
    def get_follow_state(self) -> Tuple[pygame.Vector2, float]:
        pass


class Camera:
    position: pygame.Vector2
    zoom: float
    rotation: float

    __target: Optional[CameraFollowable]

    def __init__(self, px: float = 0.0, py: float = 0.0):
        self.position = pygame.Vector2(px, py)
        self.zoom = 100.0
        self.rotation = 0.0

        self.__target = None

    def set_target(self, target: CameraFollowable) -> None:
        if not isinstance(target, CameraFollowable):
            print("Target specified is not a camera followable!")
            return

        self.__target = target

    def update(self) -> None:
        if self.__target is None:
            return
        
        self.position, self.rotation = self.__target.get_follow_state()

    def up(self) -> pygame.Vector2:
        return pygame.Vector2(0, 1).rotate_rad(self.rotation)
    
    def right(self) -> pygame.Vector2:
        return pygame.Vector2(1, 0).rotate_rad(self.rotation)
    
    def scale(self, v: pygame.Vector2 | float | int) -> pygame.Vector2 | float:
        return v * self.zoom

    def unscale(self, v: pygame.Vector2 | float | int) -> pygame.Vector2 | float:
        return v / self.zoom

    def world_to_screen(self, world_pos: pygame.Vector2, viewport: Tuple[int, int]) -> pygame.Vector2:
        relative = world_pos - self.position
        relative.y = -relative.y
        rotated = relative.rotate_rad(self.rotation)
        screen_pos = (rotated * self.zoom) + pygame.Vector2(viewport[0] / 2, viewport[1] / 2)

        return screen_pos

    def screen_to_world(self, screen_pos: pygame.Vector2, viewport: Tuple[int, int]) -> pygame.Vector2:
        rotated = (screen_pos - pygame.Vector2(viewport[0] / 2, viewport[1] / 2)) / self.zoom
        relative = rotated.rotate_rad(-self.rotation)
        relative.y = -relative.y
        world_pos = relative + self.position

        return world_pos 
        