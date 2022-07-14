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
    def __init__(self, sun):
        self.sun = sun
        self.flaresprite = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/sol_flare.png'), x=0, y=0)

    def draw(self, universe, camera):
        pos = camera.model_to_projection(self.sun.bodycentre.apos)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-camera.halfwidth, camera.halfwidth, -camera.halfheight, camera.halfheight)
        glEnable(GL_DEPTH_TEST)
        if pos[2] < 1 and pos[1] > -0.73: # Prevents labels from being drawn when they are behind the camera.
            pass
            #self.flaresprite.x=pos[0]*camera.halfwidth
            #self.flaresprite.y=pos[1]*camera.halfheight
            #self.flaresprite.scale = 50
            #self.flaresprite.draw()

def update_flux(universe, camera):
    background_strength = 0.8
    return background_strength
