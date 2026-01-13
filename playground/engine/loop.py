from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

pygame.init()

from typing import Type

from playground.engine.camera import Camera
from playground.engine.rendering import Renderer
from playground.engine.scene import Scene
from playground.engine.window import Window

scenes = []
window = Window()

def load_scene(scene: Type[Scene]):
    global scenes, window

    scenes.append(scene(window))

def run_scene(scene: Scene):
    running = True

    clock = pygame.time.Clock()

    scene.start()

    events = []

    while running:
        scene.before_update()

        events = pygame.event.get()
        scene.events = events

        scene.update()
        scene.after_update()

        scene.draw()

        for event in events:
            if event.type == pygame.QUIT:
                scene.quit()
                running = False

        events.clear()
        scene.events.clear()
        clock.tick(scene.framerate)

def run_engine():
    global scenes
    
    for s in scenes:
        run_scene(s)

    pygame.quit()