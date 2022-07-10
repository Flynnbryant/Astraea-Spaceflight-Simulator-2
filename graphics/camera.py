from pyglet import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
import pyglet
import numpy as np
from data.loading import *
from graphics.trace import *
from graphics.rings import *
from graphics.prioritiser import *
from graphics.lighting import *
from graphics.spheroid import *
from graphics.HUD_UI import *

class Camera:
    def __init__(self, window, keys, universe):
        glMatrixMode(GL_MODELVIEW)
        self.screenstate = False
        self.keys = keys
        self.window = window
        self.halfwidth = self.window.width//2
        self.halfheight = self.window.height//2
        self.invhalfwidth = 1/self.halfwidth
        self.invhalfheight = 1/self.halfheight
        self.loadingscreen = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/loadingscreen.png'), x=self.halfwidth*-0.425, y=self.halfheight*-0.985)

    def populate(self, universe):
        self.perspective = self.window.width/self.window.height
        self.pos = np.array([0., 0., -2.])
        self.camera_distance = 1e9
        self.horizontal_rot = 180.1
        self.vertical_rot = -75.1
        self.tilt = 0
        self.focus = 0
        self.fov = 45
        self.switch = False
        self.highres = False
        self.cinematic_view = False
        self.cinematic_time = 0.
        self.light = Lighting(universe.star)
        self.flare = Flare()
        self.HUD = HUD(universe, self)

        for body in universe.bodies:
            if body.name == 'Earth':
                self.background = Background(body)
        update_focus(universe, self, 0)
        self.switch = False

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

    def model_to_projection(self, apos):
        coordinate_array = np.array([*apos,1])
        proj = np.dot(coordinate_array, glGetFloatv(GL_PROJECTION_MATRIX))
        return np.array([proj[0],proj[1],proj[2]])/proj[3]

    def projection_to_model(self):
        pos = self.pos*self.inverse_scale_factor
        modelview_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
        return pos
