import pyglet
from datetime import datetime, timedelta

class HUD:
    def __init__(self, universe, camera):

        self.timestep_label = DataLabel()
        self.timestep_label.text.anchor_x = 'right'
        self.timestep_label.text.x = -camera.halfwidth*0.99
        self.timestep_label.text.y = camera.halfheight*0.93

        self.timestamp_label = DataLabel()
        self.timestep_label.text.anchor_x = 'left'
        self.timestamp_label.text.x = -camera.halfwidth*0.99
        self.timestamp_label.text.y = camera.halfheight*0.98

    def draw(self, universe, camera):
        #self.timestep_label.text.text = 'Rate: ' + str(round(universe.usertime,6)) + 'x'
        self.timestep_label.text.text = f'Rate: {str(timedelta(seconds=universe.usertime))} /s'
        self.timestep_label.text.draw()
        self.timestamp_label.text.text = datetime.utcfromtimestamp(universe.time).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
        self.timestamp_label.text.draw()

class DataLabel:
    def __init__(self):
        pyglet.font.add_directory('data/font')
        self.text = pyglet.text.Label(
            'temp',
            font_name='CMU Bright Roman',
            font_size=12,
            width = 5000,
            color = (0, 239, 255, 255),
            multiline = True,
            anchor_y='top')
