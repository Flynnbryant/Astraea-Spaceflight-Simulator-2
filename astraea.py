title = 'Astraea Spaceflight Simulator 2022'
''' Flynn Bryant        |       flynn.bryant2001@gmail.com '''
''' github.com/Flynnbryant/Astraea-Spaceflight-Simulator-2 '''

import time
import pyglet
from data.globals import *
from graphics.scene import *
from analysis.profile import *
from graphics.controls import *
from mechanics.simulation import *

def frame(dt,universe,camera):
    simulation(universe,camera,dt)
    drawScene(universe,camera)
    #key_controls(universe,camera,dt)
    universe.profile.output(dt)

universe = init_universe(focus='Saturn',profiler=False)
window = init_window(1920,1080,caption=title,resizable=True,vsync=0)
camera = init_camera(window,pyglet.window.key.KeyStateHandler(),universe)

pyglet.clock.schedule(loading_screen,universe,camera,frame)
pyglet.app.run()
