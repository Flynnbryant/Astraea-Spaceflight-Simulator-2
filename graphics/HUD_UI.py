import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from datetime import datetime, timedelta

class HUD:
    def __init__(self, universe, camera):
        self.timestep_label = DataLabel(camera,-0.99,0.93)
        self.timestamp_label = DataLabel(camera,-0.99,0.98)
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/timebackground.png'), x=-camera.halfwidth-100, y=camera.halfheight-55)
        #self.sprite = pyglet.sprite.Sprite(pyglet.resource.animation('data/sprites/catjam.gif'), x=camera.halfwidth*-1, y=camera.halfheight*0.5)
        self.sprite.scale = 0.08

    def draw(self, universe, camera):
        self.timestep_label.text.text = f'Rate: {str(timedelta(seconds=universe.usertime))} /s'
        self.timestep_label.text.draw()
        self.timestamp_label.text.text = datetime.utcfromtimestamp(universe.time).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
        self.timestamp_label.text.draw()
        self.sprite.draw()

class DataLabel:
    def __init__(self, camera, x, y):
        pyglet.font.add_directory('data/font')
        self.text = pyglet.text.Label(
            '###TEMP###',
            font_name='CMU Bright Roman',
            font_size=12,
            width = 5000,
            color = (0, 239, 255, 255),
            multiline = True,
            anchor_y='top')
        self.text.anchor_x = 'left'
        self.text.x = camera.halfwidth*x
        self.text.y = camera.halfheight*y
