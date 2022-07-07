from OpenGL.GL import *
from graphics.camera import *
import numpy as np

class Lighting:
    def __init__(self, sun):
        self.flux = 1
        self.sun = sun
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 0))
        glMaterialfv(GL_FRONT, GL_AMBIENT, (0, 0, 0, 0))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0, 0, 0, 0))

    def draw(self, universe, camera):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLight(GL_LIGHT0, GL_POSITION, (*self.sun.bodycentre.apos, 1))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE )

class Flare:
    def __init__(self):
        self.flaresprite = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/sol_flare.png'), x=0, y=0)

    def draw(self, universe, camera):
        self.flaresprite.x = 0.0*camera.halfwidth
        self.flaresprite.y = 0.0*camera.halfheight
        self.flaresprite.scale = 0.1
        #self.flaresprite.draw()
        glEnable(GL_DEPTH_TEST)

def update_flux(universe, camera):
    background_strength = 0.8
    return background_strength
