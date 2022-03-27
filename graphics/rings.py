from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image

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
        glRotatef(*self.planet.tilt_quaternion)
        glColor3f(1, 1, 1)
        gluCylinder(self.quadric, 7.45e7, 1.4092e8, 1e1, 256, 1)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
