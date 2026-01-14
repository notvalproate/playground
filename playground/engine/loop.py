from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

pygame.init()

from typing import Type

from playground.engine.scene import Scene
from playground.engine.window import Window

scenes = []
window = Window()
frame_clock = None

def load_scene(scene: Type[Scene]) -> None:
    global scenes, window

    scenes.append(scene(window))

def run_scene(scene: Scene) -> None:
    running = True

    clock = pygame.time.Clock()

    scene.start()

    events = []

    while running:
        frametime = get_frametime()
        scene.frametime = frametime

        scene.before_update()

        events = pygame.event.get()
        scene.events = events

        scene.update()

        if scene.physics is not None:
            scene.physics.step(frametime / 1000)

        scene.after_update()

        scene.draw()

        for event in events:
            if event.type == pygame.QUIT:
                scene.quit()
                running = False

        events.clear()
        scene.events.clear()
        clock.tick(scene.framerate)

def get_frametime() -> int:
    global frame_clock

    if frame_clock is None:
        frame_clock = pygame.time.get_ticks()
        return 16
    
    current_time = pygame.time.get_ticks()
    frame_time = current_time - frame_clock
    frame_clock = current_time
    return frame_time

def run_engine() -> None:
    global scenes
    
    for s in scenes:
        run_scene(s)

    pygame.quit()