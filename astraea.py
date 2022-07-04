'''
Astraea Spaceflight Simulator 2
Flynn Bryant | flynn.bryant2001@gmail.com
'''
import time
import pyglet
from data.globals import *
from graphics.scene import *
from analysis.profile import *
from interface.controls import *
from mechanics.simulation import *

def frame(dt,universe,camera):
    if camera.screenstate == 2:
        simulation(universe,dt)
        drawScene(universe,camera)
        key_controls(universe,camera,dt)
        universe.profile.output(dt)
    else:
        loading_screen(universe,camera)

title = 'Astraea Spaceflight Simulator 2022'
universe = init_universe(focus='Saturn',profiler=False)
window = init_window(1920,1080,caption=title,resizable=True,vsync=0)
camera = init_camera(window,pyglet.window.key.KeyStateHandler(),universe)

pyglet.clock.schedule(frame,universe,camera)
pyglet.app.run()
