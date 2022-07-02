'''
globals.py

Creating global objects for the universe, window, and camera classes.
This is particularly useful for the window class of type Interface,
which inherits mouse movements and actions from pyglet.window.Window.

Each function passes on the initialisation call and sets the resulting
object to global.
'''

import pyglet
from data.universe import *
from graphics.camera import *
from interface.mouse import *

def init_universe(*args, **kwargs):
    global universe
    universe = Universe(*args, **kwargs)
    return universe

def init_window(*args, **kwargs):
    global window
    window = Interface(*args, **kwargs)
    return window

def init_camera(*args, **kwargs):
    global camera
    camera = Camera(*args, **kwargs)
    return camera
