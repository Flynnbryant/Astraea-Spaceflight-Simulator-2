import pyglet
import numpy as np
from graphics.prioritiser import *
from graphics.HUD_UI import *
import data.globals

class Mouse(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,resizable=True,vsync=0,**kwargs)
        self.set_icon(pyglet.image.load('data/textures/icon.png'))
        self.dragging = False

    def mouse_precision(self, x, a, b):
        return a*b*(-x/(b+x**2) + x/b)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        update_zoom(data.globals.universe, data.globals.camera, (1+self.mouse_precision(scroll_y, 0.05, 1)))

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.dragging = True
        data.globals.camera.vertical_rot = np.clip(data.globals.camera.vertical_rot -self.mouse_precision(dy, 0.5, 100), -180, 0)
        data.globals.camera.horizontal_rot += self.mouse_precision(dx, 0.5, 100)

    def on_mouse_press(self, x, y, button, modifiers):
        if data.globals.camera.cinematic_view:
            data.globals.camera.cinematic_view = False
            update_zoom(data.globals.universe, data.globals.camera, 1)
            data.globals.camera.switch = True
        self.dragging = False
        self.scaledx = (x-data.globals.camera.halfwidth)*data.globals.camera.invhalfwidth
        self.scaledy = (y-data.globals.camera.halfheight)*data.globals.camera.invhalfheight
        if self.scaledy < -0.73:
            data.globals.camera.HUD.press_interaction(data.globals.camera, self.scaledx, self.scaledy, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.scaledx = (x-data.globals.camera.halfwidth)*data.globals.camera.invhalfwidth
        self.scaledy = (y-data.globals.camera.halfheight)*data.globals.camera.invhalfheight
        data.globals.camera.HUD.release_interaction(self.scaledx, self.scaledy, button, modifiers)
        if not self.dragging:
            if self.scaledy > -0.73:
                self.select_object()

    def select_object(self):
        if data.globals.camera.planetary_view:
            consider = [data.globals.universe.focus_entity.local_planet] + data.globals.universe.focus_entity.local_planet.satellites
        else:
            consider = data.globals.universe.star.satellites

        for object in consider:
            if data.globals.camera.camera_distance < object.outer_label_distance:
                centre = data.globals.camera.model_to_projection(object.bodycentre.apos)
                ''' This centre is different when in cinematic mode'''
                ''' Try drawing one label to see if labels change too, or if something about having to draw a label resets it '''
                if np.abs(centre[0]-self.scaledx) < 0.02 and np.abs(centre[1]-self.scaledy) < 0.1:
                    data.globals.universe.focus = object.focus_num
                    data.globals.universe.focus_entity = object
