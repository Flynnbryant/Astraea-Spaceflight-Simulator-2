import pyglet
import numpy as np
from interface.prioritiser import *
import data.globals
from interface.utilities import *

class Interface(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon(pyglet.image.load('data/textures/icon.png'))
        self.dragging = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        update_zoom(data.globals.universe, data.globals.camera, (1+mouse_precision(scroll_y, 0.05, 1)))

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.dragging = True
        data.globals.camera.vertical_rot = np.clip(data.globals.camera.vertical_rot -mouse_precision(dy, 0.5, 100), -180, 0)
        data.globals.camera.horizontal_rot += mouse_precision(dx, 0.5, 100)

    def on_mouse_press(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.dragging:
            scaledx = (x-data.globals.camera.halfwidth)*data.globals.camera.invhalfwidth
            scaledy = (y-data.globals.camera.halfheight)*data.globals.camera.invhalfheight

            if data.globals.camera.planetary_view:
                consider = [data.globals.universe.focus_entity.local_planet] + data.globals.universe.focus_entity.local_planet.satellites
            else:
                consider = data.globals.universe.star.satellites

            for object in consider:
                if data.globals.camera.camera_distance < object.outer_label_distance:
                    centre = model_to_projection(data.globals.camera, object.bodycentre.apos)
                    print(data.globals.camera.cinematic_view, object.bodycentre.apos)
                    ''' This centre is different when in cinematic mode'''
                    ''' Try drawing one label to see if labels change too, or if something about having to draw a label resets it '''
                    if np.abs(centre[0]-scaledx) < 0.02 and np.abs(centre[1]-scaledy) < 0.1:
                        data.globals.universe.focus = object.focus_num
                        data.globals.universe.focus_entity = object
