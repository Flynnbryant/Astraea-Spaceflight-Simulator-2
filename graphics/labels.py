import time
import pyglet
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from interface.utilities import *

class LabelBatch:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def draw(self, universe, camera):
        self.batch.draw()

class EntityLabel:
    def __init__(self, entity, width, height, labelbatch):
        pyglet.font.add_directory('data/font')
        self.entity = entity
        self.triangle_width = width
        self.triangle_height = height
        self.batch = labelbatch.batch
        self.text = pyglet.text.Label(
            entity.name,
            font_name='CMU Bright Roman',
            font_size=12,
            color = (*(self.entity.color*self.entity.specific_strength).astype(int), 255),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom',
            batch = self.batch)
        self.text.content_valign = 'bottom'

    def regenerate_label(self):
        self.text = pyglet.text.Label(
            self.entity.name,
            font_name='CMU Bright Roman',
            font_size=12,
            color = (*(self.entity.color*self.entity.specific_strength).astype(int), 255),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom',
            batch = self.batch)

    def recalculate_color(self):
        self.text.color = (*(self.entity.color*self.entity.specific_strength).astype(int), 255)

    def draw(self, universe, camera):
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        camera.moveCamera()
        pos = model_to_projection(camera, self.entity.bodycentre.apos + [0.,0.,self.entity.mean_radius])
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glColor3f(*(self.entity.colorsmall*self.entity.specific_strength))
        glBegin(GL_TRIANGLES) # Speed up
        glVertex3f(*pos)
        glVertex3f(pos[0]-self.triangle_width, pos[1]+self.triangle_height, pos[2])
        glVertex3f(pos[0]+self.triangle_width, pos[1]+self.triangle_height, pos[2])
        glEnd()
        gluOrtho2D(-camera.halfwidth, camera.halfwidth, -camera.halfheight, camera.halfheight)

        if pos[2] < 1: # Prevents labels from being drawn when they are behind the camera.
            self.text.x=pos[0]*camera.halfwidth
            self.text.y=(pos[1]+self.triangle_height+0.02)*camera.halfheight
            self.text.draw()
        glEnable(GL_DEPTH_TEST)
