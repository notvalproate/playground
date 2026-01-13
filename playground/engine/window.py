import pygame

class Window:
    caption: str
    width: int
    height: int
    fullscreen: bool
    surface: pygame.Surface

    def __init__(self) -> None:
        self.set_caption("Playground")
        self.fullscreen = False
        self.set_resolution(1280, 720)

    def set_caption(self, caption: str) -> None:
        self.caption = caption
        pygame.display.set_caption(self.caption)
    
    def set_resolution(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def set_fullscreen(self, fs: bool) -> None:
        self.fullscreen = fs
        flags = pygame.FULLSCREEN if fs else pygame.RESIZABLE
        self.surface = pygame.display.set_mode((self.width, self.height), flags)

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.set_fullscreen(self.fullscreen)