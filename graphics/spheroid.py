from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
from PIL import Image

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
        if self.body is universe.star:
            glDisable(GL_LIGHTING)
        else:
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

class Ring:
    def __init__(self, planet):
        self.planet = planet
        self.quadric = gluNewQuadric()
        gluQuadricTexture(self.quadric, GL_TRUE)
        img = Image.open('data/textures/RingsT.png')
        img_data = img.tobytes('raw', 'RGBA', 0, -1)
        texture = glGenTextures(1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self.texture = texture

    def draw(self, universe, camera):
        camera.moveCamera()
        glDisable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glLoadIdentity()
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glTranslatef(*self.planet.bodycentre.apos)
        glRotatef((universe.time*self.planet.satellites[0].rotation_rate)%360,*self.planet.axis_vector)
        glRotatef(*self.planet.tilt_quaternion)
        glColor3f(1, 1, 1)
        gluCylinder(self.quadric, 7.45e7, 1.4122e8, 1e1, 256, 1)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
