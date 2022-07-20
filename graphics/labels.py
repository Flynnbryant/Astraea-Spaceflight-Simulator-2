import time
import pyglet
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class EntityLabel:
    def __init__(self, entity, width, height):
        pyglet.font.add_directory('data/font')
        self.entity = entity
        self.triangle_width = width
        self.triangle_height = height
        self.text = pyglet.text.Label(
            entity.name,
            font_name='CMU Bright Roman',
            font_size=12,
            color = (*(self.entity.color).astype(int), int(255*self.entity.specific_strength)),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom')
        self.text.content_valign = 'bottom'

    def regenerate_label(self):
        self.text = pyglet.text.Label(
            self.entity.name,
            font_name='CMU Bright Roman',
            font_size=12,
            color = (*(self.entity.color).astype(int), int(255*self.entity.specific_strength)),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom')

    def draw(self, universe, camera):
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        camera.moveCamera()
        pos = camera.model_to_projection(self.entity.bodycentre.apos + [0.,0.,self.entity.mean_radius])
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        if pos[1] > -0.73:
            glLoadIdentity()
            glColor3f(*(self.entity.colorsmall*self.entity.specific_strength))
            glBegin(GL_TRIANGLES) # Speed up
            glVertex3f(*pos)
            glVertex3f(pos[0]-self.triangle_width, pos[1]+self.triangle_height, pos[2])
            glVertex3f(pos[0]+self.triangle_width, pos[1]+self.triangle_height, pos[2])
            glEnd()

        gluOrtho2D(-camera.halfwidth, camera.halfwidth, -camera.halfheight, camera.halfheight)
        if pos[2] < 1 and pos[1] > -0.73: # Prevents labels from being drawn when they are behind the camera.
            self.text.x=pos[0]*camera.halfwidth
            self.text.y=(pos[1]+self.triangle_height+0.02)*camera.halfheight
            self.text.draw()
        glEnable(GL_DEPTH_TEST)

class DataLabel:
    def __init__(self, camera, x, y, batch, group):
        pyglet.font.add_directory('data/font')
        self.text = pyglet.text.Label(
            '123456789.012',
            font_name='CMU Bright Roman',
            font_size=12,
            width = 500,
            color = (0, 239, 255, 255),
            multiline = True,
            anchor_y='top',
            batch = batch,
            group = group)
        #self.text.halign = 'right'
        self.text.anchor_x = 'left'
        self.text.x = camera.halfwidth*x
        self.text.y = camera.halfheight*y
