import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from datetime import datetime, timedelta

from graphics.labels import *
from spacecraft.node import *
from graphics.prioritiser import *

class HUD:
    def __init__(self, universe, camera):
        self.universe = universe
        self.HUDBatch = pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.OrderedGroup(0)
        self.background = pyglet.graphics.OrderedGroup(1)
        self.timestep_label = DataLabel(camera,-0.94,-0.755,self.HUDBatch,self.foreground)
        self.timestamp_label = DataLabel(camera,-0.98,-0.938,self.HUDBatch,self.foreground)
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/UI2_Spacecraft.png'), x=-camera.halfwidth*1, y=-camera.halfheight*1.05, batch=self.HUDBatch, group=self.background)
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
            'antinormal':False,
            'decrease_focus':False,
            'increase_focus':False,
            'pause_timestep':False
        }
        self.mode = self.spacecraft_control
        self.focus_left = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/focus_left.png'), x=camera.halfwidth*0.532, y=camera.halfheight*-0.92, group=self.foreground)
        self.focus_right = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/focus_right.png'), x=camera.halfwidth*0.622, y=camera.halfheight*-0.92, group=self.foreground)
        self.time_center = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/time_center.png'), x=camera.halfwidth*-0.9902, y=camera.halfheight*-0.9102, group=self.foreground)
        self.time_left_red = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/time_left_red.png'), x=camera.halfwidth*-0.9902, y=camera.halfheight*-0.9102, group=self.foreground)
        self.time_left = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/time_left.png'), x=camera.halfwidth*-0.9902, y=camera.halfheight*-0.9102, group=self.foreground)
        self.time_right_red = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/time_right_red.png'), x=camera.halfwidth*-0.9902, y=camera.halfheight*-0.9102, group=self.foreground)
        self.time_right = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/time_right.png'), x=camera.halfwidth*-0.9902, y=camera.halfheight*-0.9102, group=self.foreground)
        self.velocity_red = pyglet.sprite.Sprite(pyglet.image.load('data/sprites/velocity_red.png'), x=camera.halfwidth*-0.62, y=camera.halfheight*-0.9852, group=self.foreground)

        self.focus_left.scale = 0.75
        self.focus_right.scale = 0.75
        self.time_center.scale = 0.75
        self.time_left_red.scale = 0.75
        self.time_left.scale = 0.75
        self.time_right_red.scale = 0.75
        self.time_right.scale = 0.75
        self.velocity_red.scale = 0.75

    def draw(self, universe, camera):
        glEnable(GL_DEPTH_TEST)
        tsd = timedelta(seconds=universe.usertime)
        Sdays = str(tsd.days).zfill(3)
        hr = int(tsd.seconds/(60*60))
        Shr = str(hr).zfill(2)
        mins = int((tsd.seconds-hr*60*60)/60)
        Smins = str(mins).zfill(2)
        sec = int((tsd.seconds-hr*60*60-mins*60))
        Ssec = str(sec).zfill(2)
        Smil = str(tsd.microseconds)[0:1]
        self.timestep_label.text.text = f'{Sdays}d {Shr}:{Smins}:{Ssec}.{Smil}'
        self.timestamp_label.text.text = datetime.utcfromtimestamp(universe.time).strftime('%Y-%m-%d %H:%M:%S.%f')

        if universe.usertime > 60:
            self.velocity_red.draw()

        if self.current_actions['increase_timestep']:
            newtime = min(self.universe.usertime*1.05, 31536000)
            self.universe.usertime = newtime
            if newtime < 31536000:
                self.time_right.draw()
            else:
                self.time_right_red.draw()
        elif self.current_actions['decrease_timestep']:
            newtime = max(self.universe.usertime*0.95, 1)
            self.universe.usertime = newtime
            if newtime >1:
                self.time_left.draw()
            else:
                self.time_left_red.draw()
        elif self.current_actions['pause_timestep']:
            self.time_center.draw()
        elif self.current_actions['increase_focus']:
            self.focus_right.draw()
        elif self.current_actions['decrease_focus']:
            self.focus_left.draw()
        elif self.current_actions['prograde']:
            prograde(self.universe, self.universe.vessels[0], 9.81*self.universe.timestep)
        elif self.current_actions['retrograde']:
            prograde(self.universe, self.universe.vessels[0], -9.81*self.universe.timestep)
        elif self.current_actions['normal']:
            normal(self.universe, self.universe.vessels[0], 9.81*self.universe.timestep)
        elif self.current_actions['antinormal']:
            normal(self.universe, self.universe.vessels[0], -9.81*self.universe.timestep)
        elif self.current_actions['radialin']:
            radial(self.universe, self.universe.vessels[0], -9.81*self.universe.timestep)
        elif self.current_actions['radialout']:
            radial(self.universe, self.universe.vessels[0], 9.81*self.universe.timestep)

        self.HUDBatch.draw()
        glDisable(GL_DEPTH_TEST)

    def press_interaction(self, camera, x, y, button, modifiers):
        if x <-0.7:
            self.time_control(x)
        else:
            self.mode(camera, x, y, button, modifiers)

    def time_control(self,x):
        if x < -0.88:
            self.current_actions['decrease_timestep'] = True
        elif x <-0.8:
            self.universe.usertime = 1
            self.current_actions['pause_timestep'] = True
        else:
            self.current_actions['increase_timestep'] = True

    def spacecraft_control(self, camera, x, y, button, modifiers):
        if x < -0.46 and x > -0.616 and self.universe.usertime < 60:
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
        elif x > 0.29 and x < 0.51:
            if not camera.switch:
                camera.cinematic_view = True
                update_zoom(self.universe, camera, 1)
            camera.switch = False
        elif x > 0.53 and x < 0.62:
            self.current_actions['decrease_focus'] = True
            update_focus(self.universe, camera, -1)
        elif x > 0.62 and x < 0.705:
            self.current_actions['increase_focus'] = True
            update_focus(self.universe, camera, 1)

    def release_interaction(self, x, y, button, modifiers):
        self.current_actions = dict.fromkeys(self.current_actions, False)
