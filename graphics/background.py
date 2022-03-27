from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
from analysis.profile import *

class Background:
    def __init__(self, earth):
        self.axis_vector = earth.axis_vector
        self.tilt_quaternion = earth.tilt_quaternion
        self.strength = [1,1,1]
        self.size = 1
        self.galaxyQuadric = gluNewQuadric()
        gluQuadricTexture(self.galaxyQuadric, GL_TRUE)

    def draw(self, universe, camera):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.fov, camera.perspective, 0.000007, 2000.0)
        glRotatef(camera.tilt, 0, 1, 0)
        glRotatef(camera.vertical_rot, 1, 0, 0)
        glRotatef(camera.horizontal_rot, 0, 0, 1)
        glScalef(camera.scale_factor, camera.scale_factor, camera.scale_factor)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.star_texture)
        glRotatef(0,*self.axis_vector)
        glRotatef(*self.tilt_quaternion)
        glColor3f(*self.strength)
        gluSphere(self.galaxyQuadric, self.size, 128, 32)
        glDisable(GL_TEXTURE_2D)
