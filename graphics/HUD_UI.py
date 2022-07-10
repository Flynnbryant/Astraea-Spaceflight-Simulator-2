import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from datetime import datetime, timedelta

from graphics.labels import *
from spacecraft.node import *

class HUD:
    def __init__(self, universe, camera):
        self.universe = universe
        self.HUDBatch = pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.OrderedGroup(0)
        self.background = pyglet.graphics.OrderedGroup(1)
        self.timestep_label = DataLabel(camera,-0.9,-0.75,self.HUDBatch,self.foreground)
        self.timestamp_label = DataLabel(camera,-0.98,-0.938,self.HUDBatch,self.foreground)
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/UI1_Spacecraft.png'), x=-camera.halfwidth*1, y=-camera.halfheight*1.05, batch=self.HUDBatch, group=self.background)
        #self.sprite = pyglet.sprite.Sprite(pyglet.resource.animation('data/sprites/catjam.gif'), x=camera.halfwidth*-1, y=camera.halfheight*0.5)
        self.sprite.scale = 0.75
        self.current_actions = {
            'decrease_timestep':False,
            'increase_timestep':False,
            'prograde':False,
            'retrograde':False,
            'radialin':False,
            'radialout':False,
            'normal':False,
            'antinormal':False
        }
        self.mode = self.spacecraft_control

    def draw(self, universe, camera):
        glEnable(GL_DEPTH_TEST)
        self.timestep_label.text.text = str(timedelta(seconds=universe.usertime))
        self.timestamp_label.text.text = datetime.utcfromtimestamp(universe.time).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.HUDBatch.draw()
        glDisable(GL_DEPTH_TEST)
        if self.current_actions['increase_timestep']:
            self.universe.usertime = min(self.universe.usertime*(1.05), 31536000)
        elif self.current_actions['decrease_timestep']:
            self.universe.usertime = max(self.universe.usertime*(0.95), 1)
        if self.current_actions['prograde']:
            prograde(self.universe, self.universe.vessels[0], min(self.universe.timestep,np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))
        elif self.current_actions['retrograde']:
            prograde(self.universe, self.universe.vessels[0], max(-self.universe.timestep,-np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))
        elif self.current_actions['normal']:
            normal(self.universe, self.universe.vessels[0], min(self.universe.timestep,np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))
        elif self.current_actions['antinormal']:
            normal(self.universe, self.universe.vessels[0], max(-self.universe.timestep,-np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))
        elif self.current_actions['radialin']:
            radial(self.universe, self.universe.vessels[0], min(-self.universe.timestep,-np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))
        elif self.current_actions['radialout']:
            radial(self.universe, self.universe.vessels[0], max(self.universe.timestep,np.linalg.norm(self.universe.vessels[0].bodycentre.rvel*1)))

    def press_interaction(self, x, y, button, modifiers):
        if x <-0.7:
            self.time_control(x)
        else:
            self.mode(x, y, button, modifiers)

    def time_control(self,x):
        if x < -0.88:
            self.current_actions['decrease_timestep'] = True
        elif x <-0.8:
            self.universe.usertime = 1
        else:
            self.current_actions['increase_timestep'] = True

    def spacecraft_control(self, x, y, button, modifiers):
        if x < -0.46 and x > -0.616:
            if x <-0.56 and y >-0.87:
                self.current_actions['normal'] = True
            elif x <-0.56 and y <-0.87:
                self.current_actions['radialin'] = True
            elif x <-0.517 and y >-0.87:
                self.current_actions['prograde'] = True
            elif x <-0.517 and y <-0.87:
                self.current_actions['retrograde'] = True
            elif y >-0.87:
                self.current_actions['radialout'] = True
            else:
                self.current_actions['antinormal'] = True

    def release_interaction(self, x, y, button, modifiers):
        self.current_actions = dict.fromkeys(self.current_actions, False)
