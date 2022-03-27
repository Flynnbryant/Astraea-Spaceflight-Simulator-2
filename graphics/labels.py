import time
import pyglet
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from interface.utilities import *

class EntityLabel:
    def __init__(self, entity, width, height):
        self.entity = entity
        self.triangle_width = width
        self.triangle_height = height
        self.label = pyglet.text.Label(
            entity.name,
            font_name='Arial',
            font_size=10,
            color = (*(self.entity.color*self.entity.specific_strength).astype(int), 255),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom')
        self.label.content_valign = 'bottom'

    def regenerate_label(self):
        self.label = pyglet.text.Label(
            self.entity.name,
            font_name='Arial',
            font_size=10,
            color = (*(self.entity.color*self.entity.specific_strength).astype(int), 255),
            width=20,
            height=10,
            align='center',
            anchor_x='center', anchor_y='bottom')

    def draw(self, universe, camera):
        #print(f'0: {time.time()}')
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        camera.moveCamera()
        #print(f'1: {time.time()}')
        pos = model_to_projection(camera, self.entity.bodycentre.apos + [0.,0.,self.entity.mean_radius])
        #print(f'2: {time.time()}')
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glColor3f(*(self.entity.colorsmall*self.entity.specific_strength))
        #print(f'3: {time.time()}')
        glBegin(GL_TRIANGLES) # Speed up
        glVertex3f(*pos)
        glVertex3f(pos[0]-self.triangle_width, pos[1]+self.triangle_height, pos[2])
        glVertex3f(pos[0]+self.triangle_width, pos[1]+self.triangle_height, pos[2])
        glEnd()
        #print(f'4: {time.time()}')
        gluOrtho2D(-camera.halfwidth, camera.halfwidth, -camera.halfheight, camera.halfheight)
        if pos[2] < 1: # Prevents labels from being drawn when they are behind the camera.
            self.entity.label.x=pos[0]*camera.halfwidth
            self.entity.label.y=(pos[1]+self.triangle_height+0.02)*(camera.halfheight)
            self.label.draw()
        glEnable(GL_DEPTH_TEST)
        #print(f'5: {time.time()}')
