from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *

class Spheroid:
    def __init__(self, body):
        self.body = body
        self.display_obj = gluNewQuadric()
        self.tidally_locked = False
        gluQuadricTexture(self.display_obj, GL_TRUE)

    def draw(self, universe, camera):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.fov, camera.perspective, 0.000007, 2000.0)
        glTranslatef(*camera.pos)
        glRotatef(camera.tilt, 0, 1, 0)
        glRotatef(camera.vertical_rot, 1, 0, 0)
        glRotatef(camera.horizontal_rot, 0, 0, 1)
        glScalef(camera.scale_factor, camera.scale_factor, camera.scale_factor)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.body.texture)
        glColor3f(1,1,1)
        glTranslatef(*self.body.bodycentre.apos)
        glRotatef((universe.time*self.body.rotation_rate+self.body.shift)%360,*self.body.axis_vector)
        glRotatef(*self.body.tilt_quaternion)
        glScalef(*self.body.radii)
        gluSphere(self.display_obj, 1., self.render_detail*2, self.render_detail)
        glDisable(GL_TEXTURE_2D)

    def calculate_render_detail(self, universe, camera):
        if self.body.primary.object.name == 'Sol':
            self.render_detail = 64
        else:
            self.render_detail = 16

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
        gluSphere(self.galaxyQuadric, self.size, 64, 32)
        glDisable(GL_TEXTURE_2D)
