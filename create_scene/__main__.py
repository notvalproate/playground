import sys
from pathlib import Path

INIT_TEMPLATE = """from .scene import {class_name}

__all__ = ["{class_name}"]
"""

TEMPLATE = """import pygame
from typing import override

from playground.engine.scene import Scene
from playground.engine.window import Window


class {class_name}(Scene):
    position: pygame.Vector2
    delta: float

    def __init__(self, window: Window):
        do_physics = False
        super().__init__(window, do_physics)

        self.position = pygame.Vector2(0, 0)
        self.delta = 0.05

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
            "Welcome to the Playground",
            pygame.Vector2(0.0, 2.5),
        )
        self.renderer.swap_display_buffers()
"""


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m create_scene <scene_name>")
        sys.exit(1)

    scene_name = sys.argv[1]
    class_name = scene_name.capitalize() + "Scene"

    base_path = Path("playground/scenes") / scene_name
    assets_path = base_path / "assets"
    scene_file = base_path / "scene.py"
    init_file = base_path / "__init__.py"

    if base_path.exists():
        print(f"Scene '{scene_name}' already exists.")
        sys.exit(1)

    assets_path.mkdir(parents=True)
    scene_file.write_text(TEMPLATE.format(class_name=class_name))
    init_file.write_text(INIT_TEMPLATE.format(class_name=class_name))

    print(f"✔ Scene '{scene_name}' created successfully")


if __name__ == "__main__":
    main()
