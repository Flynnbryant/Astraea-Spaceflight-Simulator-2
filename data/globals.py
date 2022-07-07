'''
globals.py

Creating global objects for the universe, window, and camera classes.
This is particularly useful for the window class of type Mouse,
which inherits mouse movements and actions from pyglet.window.Window.

Each function passes on the initialisation call and sets the resulting
object to global.
'''

import pyglet
from data.universe import *
from graphics.camera import *
from graphics.mouse import *

def init_universe(*args, **kwargs):
    global universe
    universe = Universe(*args, **kwargs)
    return universe

def init_window(*args, **kwargs):
    global window
    window = Mouse(*args, **kwargs)
    return window

def init_camera(*args, **kwargs):
    global camera
    camera = Camera(*args, **kwargs)
    return camera
