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
    window.set_icon(pyglet.image.load('data/textures/icon.png'))
    #window.set_caption('Astraea Space')
    return window

def init_camera(*args, **kwargs):
    global camera
    camera = Camera(*args, **kwargs)
    return camera
