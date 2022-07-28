title = 'Astraea Spaceflight Simulator 2022'
''' Flynn Bryant - flynn.bryant2001@gmail.com '''
''' github.com/Flynnbryant/Astraea-Spaceflight-Simulator-2 '''

import pyglet
from data.universe import *
from graphics.camera import *
from graphics.mouse import *
from analysis.profile import *
from mechanics.simulation import *

def frame(dt,universe,camera):
    simulation(universe,camera,dt)
    drawScene(universe,camera)
    universe.profile.output(dt)

universe = Universe(focus='Luna',profile=False)
window = Mouse(universe,1920,1080,caption=title)
camera = Camera(universe,window)

pyglet.clock.schedule(loading_screen,universe,camera,frame)
pyglet.app.run()
