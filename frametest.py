''' Frametest '''

import time
import pyglet
from data.globals import *
from analysis.profile import *

def frame(dt,universe,camera):
    universe.profile.add('fram')
    controls(universe,camera,dt)
    universe.profile.output(dt)

title = 'Astraea Spaceflight Simulator v3.1'
universe = init_universe(focus='Saturn',profiler=True)
window = init_window(1920,1080,caption=title,resizable=True,vsync=0)
camera = init_camera(window,pyglet.window.key.KeyStateHandler(),universe)

pyglet.clock.schedule(frame,universe,camera)
pyglet.app.run()
