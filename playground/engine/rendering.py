import pygame
import math
from pathlib import Path
from typing import Tuple, Any, overload
from abc import ABC, abstractmethod
from playground.engine.camera import Camera

DEFAULT_RENDER_COLOR = (200, 0, 0)
DEFAULT_LINE_WIDTH = 1
DEFAULT_WORLD_LINE_WIDTH = 0.05
DEFAULT_FONT = None

class Sprite:
    image: pygame.Surface
    texture: pygame.Surface
    size: pygame.Vector2
    offset = pygame.Vector2

    @overload
    def __init__(self, sprite_path: str, size: pygame.Vector2 = pygame.Vector2(1, 1), offset: pygame.Vector2 = pygame.Vector2(0, 0)): ...

    @overload
    def __init__(self, surface: pygame.Surface, size: pygame.Vector2 = pygame.Vector2(1, 1), offset: pygame.Vector2 = pygame.Vector2(0, 0)): ...

    def __init__(self, sprite_input: str | pygame.Surface, size: pygame.Vector2 = pygame.Vector2(1, 1), offset: pygame.Vector2 = pygame.Vector2(0, 0)):
        if isinstance(sprite_input, str) or isinstance(sprite_input, Path):
            self.src_image = pygame.image.load(sprite_input)
        elif isinstance(sprite_input, pygame.Surface):
            self.src_image = sprite_input
        else:
            raise ValueError("Invalid input type for sprite_input. Expected a path to file or pygame.Surface.")
        
        self.src_image.set_colorkey((0, 0, 0, 0))
        self.texture = self.src_image.copy()
        self.size = size
        self.offset = offset

    def __getstate__(self) -> dict[str | Any]:
        state = self.__dict__.copy()
        src_image = state.pop("src_image")
        state["src_string"] = (pygame.image.tostring(src_image, "RGBA"), src_image.get_size())
        texture = state.pop("texture")
        state["tex_string"] = (pygame.image.tostring(texture, "RGBA"), texture.get_size())
        return state

    def __setstate__(self, state) -> None:
        src_string, src_size = state.pop("src_string")
        state["src_image"] = pygame.image.fromstring(src_string, src_size, "RGBA")
        tex_string, tex_size = state.pop("tex_string")
        state["texture"] = pygame.image.fromstring(tex_string, tex_size, "RGBA")
        self.__dict__.update(state)

    def resize_texture(self, width: int, height: int) -> None:
        self.texture = pygame.transform.scale(self.src_image, (width, height))


class Renderer:
    clear_color: Tuple[int, int, int]

    __active_surface: pygame.Surface
    __active_camera: Camera
    __viewport: Tuple[int, int]
    
    def __init__(self, surface: pygame.Surface, camera: Camera, clear_color: Tuple[int, int, int] = (240, 240, 240)):
        global DEFAULT_FONT
        DEFAULT_FONT = pygame.font.SysFont('Arial', 32)
        
        self.clear_color = clear_color

        self.__active_surface = surface
        self.__active_camera = camera
        self.__viewport = surface.get_size()

    def set_active_camera(self, camera: Camera) -> None:
        if not isinstance(camera, Camera):
            print("Camera passed is not an instance of the Camera class!")
            return

        self.__active_camera = camera

    def set_active_surface(self, surface: pygame.Surface) -> None:
        if not isinstance(surface, pygame.Surface):
            print("Surface pass is not an instance of the PyGame Surface class!")
            return
        
        self.__active_surface = surface
        self.__viewport = surface.get_size()

    def get_active_surface(self) -> pygame.Surface:
        return self.__active_surface

    def clear(self) -> None:
        self.__active_surface.fill(self.clear_color)

    def swap_display_buffers(self) -> None:
        pygame.display.flip()

    def draw_sprite(
        self,
        sprite: Sprite,
        world_coords: pygame.Vector2 = pygame.Vector2(0, 0),
        rotation: float = 0,
        flags: int = 0
    ) -> None:
        tex_size = sprite.texture.get_size()
 
        scaled_size = self.__active_camera.scale(sprite.size)
        scaled_width = int(round(scaled_size.x))
        scaled_height = int(round(scaled_size.y))

        if scaled_width != tex_size[0]:
            sprite.resize_texture(scaled_width, scaled_height)

        self.blit_surface_world(sprite.texture, world_coords + sprite.offset, rotation, None, flags)

    def blit_surface(
        self, 
        surface: pygame.Surface, 
        coords: pygame.Vector2 = pygame.Vector2(0, 0),
        rotation: float = 0,
        area: Tuple[int, int, int, int] | None = None, 
        flags: int = 0
    ) -> None:
        surface = pygame.transform.rotate(surface, rotation * 180 / math.pi)
        self.__active_surface.blit(surface, (coords.x, coords.y), area, flags)

    def blit_surface_world(
        self, 
        surface: pygame.Surface,
        world_coords: pygame.Vector2 = pygame.Vector2(0, 0),
        rotation: float = 0,
        area: Tuple[int, int, int, int] | None = None, 
        flags: int = 0
    ) -> None:
        screen_coords = self.__active_camera.world_to_screen(world_coords, self.__viewport)
        surface = pygame.transform.rotate(surface, -(self.__active_camera.rotation - rotation) * 180 / math.pi)

        s_width, s_height = surface.get_size()
        screen_coords.x -= s_width / 2
        screen_coords.y -= s_height / 2

        self.__active_surface.blit(surface, (screen_coords.x, screen_coords.y), area, flags)

    def draw_text(
        self, 
        text: str,
        coords: pygame.Vector2 = pygame.Vector2(0, 0),
        font: pygame.font.Font = None, 
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR,
        bg_color: Tuple[int, int, int, int] | None = None,
        flags: int = 0
    ) -> None:
        if font is None:
            font = DEFAULT_FONT

        rendered_text = font.render(text, True, color, bg_color)
        self.__active_surface.blit(rendered_text, (coords.x, coords.y), None, flags)

    def draw_text_world(
        self, 
        text: str,
        world_coords: pygame.Vector2 = pygame.Vector2(0, 0),
        rotation: float = 0,
        font: pygame.font.Font = None, 
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR,
        bg_color: Tuple[int, int, int, int] | None = None,
        flags: int = 0
    ) -> None:
        if font is None:
            font = DEFAULT_FONT
            
        rendered_text = font.render(text, True, color, bg_color)
        self.blit_surface_world(rendered_text, world_coords, rotation, None, flags)

    def draw_line(
        self,
        start_pos: pygame.Vector2,
        end_pos: pygame.Vector2,
        width: float = DEFAULT_LINE_WIDTH,
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR
    ) -> None:
        pygame.draw.line(self.__active_surface, color, (start_pos.x, start_pos.y), (end_pos.x, end_pos.y), int(round(width)))

    def draw_line_world(
        self,
        start_pos: pygame.Vector2,
        end_pos: pygame.Vector2,
        width: float = DEFAULT_WORLD_LINE_WIDTH,
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR
    ) -> None:
        start_pos = self.__active_camera.world_to_screen(start_pos, self.__viewport)
        end_pos = self.__active_camera.world_to_screen(end_pos, self.__viewport)
        width_scaled = self.__active_camera.scale(width)

        pygame.draw.line(self.__active_surface, color, (start_pos.x, start_pos.y), (end_pos.x, end_pos.y), int(round(width_scaled)))

    def draw_circle_fill(
        self,
        center: pygame.Vector2,
        radius: float,
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False
    ) -> None:
        circle_center = self.__active_camera.world_to_screen(center, self.__viewport)
        radius_scaled = self.__active_camera.scale(radius)
        
        pygame.draw.circle(self.__active_surface, color, (circle_center.x, circle_center.y), radius_scaled, 0, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)

    def draw_circle_outline(
        self,
        center: pygame.Vector2,
        radius: float,
        width: float = DEFAULT_WORLD_LINE_WIDTH,
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False
    ) -> None:
        circle_center = self.__active_camera.world_to_screen(center, self.__viewport)
        radius_scaled = self.__active_camera.scale(radius)
        width_scaled = self.__active_camera.scale(width)

        pygame.draw.circle(self.__active_surface, color, (circle_center.x, circle_center.y), radius_scaled, int(round(width_scaled)), draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)

    def draw_rect_fill(
        self, 
        rect: Tuple[int, int, int, int],
        rotation: float = 0,
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR, 
        border_radius: int = -1
    ) -> None:
        rect_size = self.__active_camera.scale(pygame.Vector2(rect[2], rect[3]))
        border_scaled = self.__active_camera.scale(border_radius)
        rect_surface = pygame.Surface((rect_size.x, rect_size.y))
        rect_surface.set_colorkey((0, 0, 0, 0))
        pygame.draw.rect(rect_surface, color, (0, 0, rect_size.x, rect_size.y), 0, int(round(border_scaled)))
        rect_surface = pygame.transform.rotate(rect_surface, rotation * 180 / math.pi)

        self.blit_surface_world(rect_surface, pygame.Vector2(0, 0))

    def draw_rect_outline(
        self, 
        rect: Tuple[int, int, int, int], 
        width: float = DEFAULT_WORLD_LINE_WIDTH, 
        color: Tuple[int, int, int] = DEFAULT_RENDER_COLOR, 
        border_radius: int = -1
    ) -> None:
        rect_coords = self.__active_camera.world_to_screen(pygame.Vector2(rect[0], rect[1]), self.__viewport)
        rect_dimensions = self.__active_camera.scale(pygame.Vector2(rect[2], rect[3]))
        border_scaled = self.__active_camera.scale(border_radius)
        width_scaled = self.__active_camera.scale(width)

        pygame.draw.rect(self.__active_surface, color, (rect_coords.x, rect_coords.y, rect_dimensions.x, rect_dimensions.y), int(round(width_scaled)), int(round(border_scaled)))
