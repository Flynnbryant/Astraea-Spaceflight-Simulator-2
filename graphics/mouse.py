import pyglet
import numpy as np
from graphics.prioritiser import *
from graphics.HUD_UI import *

class Mouse(pyglet.window.Window):
    def __init__(self, universe, *args, **kwargs):
        #config = pyglet.gl.Config() #sample_buffers=1, samples=2
        #super().__init__(*args,resizable=True,vsync=0,config=config,**kwargs)
        super().__init__(*args,resizable=True,vsync=0,**kwargs)
        self.set_icon(pyglet.image.load('data/textures/icon.png'))
        self.universe = universe
        self.dragging = False

    def mouse_precision(self, x, a, b):
        return a*b*(-x/(b+x**2) + x/b)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        update_zoom(self.universe, self.camera, (1+self.mouse_precision(scroll_y, 0.05, 1)))

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.dragging = True
        self.camera.vertical_rot = np.clip(self.camera.vertical_rot -self.mouse_precision(dy, 0.5, 100), -180, 0)
        self.camera.horizontal_rot += self.mouse_precision(dx, 0.5, 100)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.camera.cinematic_view:
            self.camera.cinematic_view = False
            update_zoom(self.universe, self.camera, 1)
            self.camera.switch = True
        self.dragging = False
        self.scaledx = (x-self.camera.halfwidth)*self.camera.invhalfwidth
        self.scaledy = (y-self.camera.halfheight)*self.camera.invhalfheight
        if self.scaledy < -0.73:
            self.camera.HUD.press_interaction(self.camera, self.scaledx, self.scaledy, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.scaledx = (x-self.camera.halfwidth)*self.camera.invhalfwidth
        self.scaledy = (y-self.camera.halfheight)*self.camera.invhalfheight
        self.camera.HUD.release_interaction(self.scaledx, self.scaledy, button, modifiers)
        if not self.dragging:
            if self.scaledy > -0.73:
                self.select_object()

    def select_object(self):
        if self.camera.planetary_view:
            consider = [self.universe.focus_entity.local_planet] + self.universe.focus_entity.local_planet.satellites
        else:
            consider = self.universe.star.satellites

        for object in consider:
            if self.camera.camera_distance < object.outer_label_distance:
                centre = self.camera.model_to_projection(object.bodycentre.apos)
                ''' This centre is different when in cinematic mode'''
                ''' Try drawing one label to see if labels change too, or if something about having to draw a label resets it '''
                if np.abs(centre[0]-self.scaledx) < 0.02 and np.abs(centre[1]-self.scaledy) < 0.1:
                    self.universe.focus = object.focus_num
                    self.universe.focus_entity = object
