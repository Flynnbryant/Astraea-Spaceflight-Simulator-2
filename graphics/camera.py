from pyglet import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
import pyglet
import numpy as np
from interface.controls import *
from data.loading import *
from graphics.trace import *
from graphics.rings import *
from interface.prioritiser import *
from graphics.lighting import *
from graphics.background import *
from interface.utilities import *

import time

class Camera:
    def __init__(self, window, keys, universe):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.keys = keys
        self.window = window
        self.halfwidth = self.window.width//2
        self.halfheight = self.window.height//2
        self.invhalfwidth = 1/self.halfwidth
        self.invhalfheight = 1/self.halfheight
        self.perspective = self.window.width/self.window.height
        self.pos = np.array([0., 0., -2.])
        self.camera_distance = 1e8
        self.horizontal_rot = 180
        self.vertical_rot = -75
        self.tilt = 0
        self.focus = 0
        self.fov = 45
        self.switch = False
        self.highres = False
        self.cinematic_view = False
        self.cinematic_time = 0.
        self.light = Lighting(universe.star)
        self.flare = Flare()
        for body in universe.bodies:
            if body.name == 'Earth':
                self.background = Background(body)
        update_focus(universe, self, 0)
        self.switch = False
        load_textures(universe, self)
        #self.screen = (pyglet.canvas.Display()).get_default_screen() <- Probably for interface

    def moveCamera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glTranslatef(0, 0, 0)
        gluPerspective(self.fov, self.perspective, 0.000007, 2000.0)
        #glFrustum(-0.0001,0.0001,-0.0001,0.0001,0.001, 2000.0)
        glTranslatef(*self.pos)
        glRotatef(self.tilt, 0, 1, 0)
        glRotatef(self.vertical_rot, 1, 0, 0)
        glRotatef(self.horizontal_rot, 0, 0, 1)
        glScalef(self.scale_factor, self.scale_factor, self.scale_factor)
