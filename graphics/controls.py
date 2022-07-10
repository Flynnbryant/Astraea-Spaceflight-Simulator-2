import numpy as np
import time
import pyglet
from graphics.prioritiser import *
from spacecraft.node import *
from graphics.mouse import *

def key_controls(universe, camera, dt):
    camera.window.push_handlers(camera.keys)
    if any(camera.keys):
        simulation_keys(universe, camera, dt)
        vessel_keys(universe, camera, dt)
        if camera.keys[pyglet.window.key.LSHIFT]:
            precise_keys(universe, camera, dt)
        else:
            camera_keys(universe, camera, dt)
    universe.profile.add('con')

def simulation_keys(universe, camera, dt):
    if camera.keys[pyglet.window.key.F] or camera.keys[pyglet.window.key.BRACKETLEFT]:
        update_focus(universe, camera, -1)
    elif camera.keys[pyglet.window.key.G] or camera.keys[pyglet.window.key.BRACKETRIGHT]:
        update_focus(universe, camera, 1)
    elif camera.keys[pyglet.window.key.C]:
        if not camera.switch:
            camera.cinematic_view = not camera.cinematic_view
            camera.switch = True
            update_zoom(universe, camera, 1)
    else:
        camera.switch = False
