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
        self.press_mode = self.spacecraft_control
        self.draw_mode = self.spacecraft_draw
        self.HUDBatch = pyglet.graphics.Batch()
        self.TextBatch= pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.background = pyglet.graphics.OrderedGroup(2)
        self.timestamp_label = DataLabel(camera,-0.99,-0.935,self.TextBatch,self.foreground)
        self.timestep_label = DataLabel(camera,-0.948,-0.758,self.TextBatch,self.foreground)
        self.timestep_label.text.text = update_timestep_label(universe.usertime)
        self.current_actions = dict.fromkeys(['decrease_timestep','increase_timestep','prograde','retrograde','radialin','radialout','normal','antinormal','decrease_focus','increase_focus','pause_timestep'],False)

        self.camera_background      = sprite_loader(camera, 'UI3_camera_normal'     ,-0.68   ,-1.005  ,0.43,self.background,batch=self.HUDBatch)
        self.spacecraft_background  = sprite_loader(camera, 'UI3_spacecraft_normal' ,-0.68   ,-1.01  ,0.43,self.background)
        self.parameters_background  = sprite_loader(camera, 'UI3_parameters_normal' ,-0.68   ,-1.015  ,0.43,self.background)

        self.time_background        = sprite_loader(camera, 'UI3_time_normal'       ,-1.02  ,-1.01  ,0.43,self.midground,batch=self.HUDBatch)
        self.time_center            = sprite_loader(camera, 'UI3_time_center'       ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_right             = sprite_loader(camera, 'UI3_time_right'        ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_rightR            = sprite_loader(camera, 'UI3_time_rightR'       ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_left              = sprite_loader(camera, 'UI3_time_left'         ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_leftR             = sprite_loader(camera, 'UI3_time_leftR'        ,-1.02  ,-1.01  ,0.43,self.midground)

        self.focus_left             = sprite_loader(camera, 'focus_left'        ,0.532  ,-0.92  ,0.75,self.background)
        self.focus_right            = sprite_loader(camera, 'focus_right'       ,0.622  ,-0.92  ,0.75,self.background)
        self.velocity_red           = sprite_loader(camera, 'velocity_red'      ,-0.62  ,-0.9852,0.75,self.background)

    def draw(self, universe, camera):
        glEnable(GL_DEPTH_TEST)
        self.TextBatch.draw()
        self.time_draw(universe, camera)
        self.draw_mode(universe, camera)
        self.HUDBatch.draw()
        glDisable(GL_DEPTH_TEST)

    def press_interaction(self, camera, x, y, button, modifiers):
        if x <-0.7:
            self.time_control(x)
        elif x >0.7:
            self.menu_control(y)
        else:
            self.press_mode(camera, x, y, button, modifiers)

    def time_control(self,x):
        if x < -0.9:
            self.current_actions['decrease_timestep'] = True
        elif x <-0.8:
            self.universe.usertime = 1
            self.timestep_label.text.text = update_timestep_label(self.universe.usertime)
            self.current_actions['pause_timestep'] = True
        else:
            self.current_actions['increase_timestep'] = True

    def menu_control(self,y):
        if y > -0.83:
            self.press_mode = self.camera_control
            self.draw_mode = self.camera_draw
            self.camera_background.batch = self.HUDBatch
            self.spacecraft_background.batch = None
            self.parameters_background.batch = None
        elif y > -0.92:
            self.press_mode = self.spacecraft_control
            self.draw_mode = self.spacecraft_draw
            self.camera_background.batch = None
            self.spacecraft_background.batch = self.HUDBatch
            self.parameters_background.batch = None
        else:
            self.press_mode = self.parameters_control
            self.draw_mode = self.parameters_draw
            self.camera_background.batch = None
            self.spacecraft_background.batch = None
            self.parameters_background.batch = self.HUDBatch

    def camera_control(self, camera, x, y, button, modifiers):
        pass

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

    def parameters_control(self, camera, x, y, button, modifiers):
        pass

    def time_draw(self, universe, camera):
        self.timestamp_label.text.text = datetime.utcfromtimestamp(universe.time).strftime('%Y-%m-%d %H:%M:%S.%f')
        if True in self.current_actions.values():
            if self.current_actions['increase_timestep']:
                newtime = min(self.universe.usertime*1.05, 31536000)
                self.universe.usertime = newtime
                self.timestep_label.text.text = update_timestep_label(universe.usertime)
                if newtime < 31536000:
                    self.time_right.draw()
                else:
                    self.time_rightR.draw()
            elif self.current_actions['decrease_timestep']:
                newtime = max(self.universe.usertime*0.95, 0.01)
                self.universe.usertime = newtime
                self.timestep_label.text.text = update_timestep_label(universe.usertime)
                if newtime >0.01:
                    self.time_left.draw()
                else:
                    self.time_leftR.draw()
            elif self.current_actions['pause_timestep']:
                self.time_center.draw()

    def camera_draw(self, universe, camera):
        pass

    def spacecraft_draw(self, universe, camera):
        if universe.usertime > 60:
            self.velocity_red.draw()
        if True in self.current_actions.values():
            if self.current_actions['increase_focus']:
                self.focus_right.draw()
            elif self.current_actions['decrease_focus']:
                self.focus_left.draw()
            elif self.current_actions['prograde']:
                prograde(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)
            elif self.current_actions['retrograde']:
                prograde(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
            elif self.current_actions['normal']:
                normal(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)
            elif self.current_actions['antinormal']:
                normal(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
            elif self.current_actions['radialin']:
                radial(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
            elif self.current_actions['radialout']:
                radial(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)

    def parameters_draw(self, universe, camera):
        pass

    def release_interaction(self, x, y, button, modifiers):
        self.current_actions = dict.fromkeys(self.current_actions, False)

def update_timestep_label(timestep):
    tsd = timedelta(seconds=timestep)
    hr = int(tsd.seconds/(60*60))
    mins = int((tsd.seconds-hr*60*60)/60)
    sec = int((tsd.seconds-hr*60*60-mins*60))
    return f'{str(tsd.days).zfill(3)}d {str(hr).zfill(2)}:{str(mins).zfill(2)}:{str(sec).zfill(2)}.{str(tsd.microseconds).zfill(6)[:2]}'

def sprite_loader(camera, name, x, y, scale, group, batch=None, type='.png'):
    spriteobject = pyglet.sprite.Sprite(pyglet.image.load(f'data/sprites/{name}{type}'), x=camera.halfwidth*x, y=camera.halfheight*y, group=group, batch=batch)
    spriteobject.scale = scale
    return spriteobject

#self.sprite = pyglet.sprite.Sprite(pyglet.resource.animation('data/sprites/catjam.gif'), x=camera.halfwidth*-1, y=camera.halfheight*0.5)
