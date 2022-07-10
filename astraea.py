title = 'Astraea Spaceflight Simulator 2022'
''' Flynn Bryant - flynn.bryant2001@gmail.com '''
''' github.com/Flynnbryant/Astraea-Spaceflight-Simulator-2 '''

import pyglet
from data.globals import *
from graphics.scene import *
from analysis.profile import *
from mechanics.simulation import *

def frame(dt,universe,camera):
    simulation(universe,camera,dt)
    drawScene(universe,camera)
    universe.profile.output(dt)

universe = init_universe(focus='Saturn',profile=True)
window = init_window(1920,1080,caption=title)
camera = init_camera(universe,window)

pyglet.clock.schedule(loading_screen,universe,camera,frame)
pyglet.app.run()
