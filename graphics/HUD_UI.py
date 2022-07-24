import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from datetime import datetime, timedelta
from decimal import Decimal

from graphics.labels import *
from spacecraft.node import *
from graphics.prioritiser import *
from spacecraft.vessel import *

class HUD:
    def __init__(self, universe, camera):
        self.universe = universe
        self.press_mode = self.camera_control
        self.draw_mode = self.camera_draw
        self.HUDBatch = pyglet.graphics.Batch()
        self.TextBatch= pyglet.graphics.Batch()
        self.ParameterBatch = pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.background = pyglet.graphics.OrderedGroup(2)
        self.timestamp_label = DataLabel(camera,-0.99,-0.935,self.TextBatch,self.foreground)
        self.timestep_label = DataLabel(camera,-0.948,-0.758,self.TextBatch,self.foreground)
        self.timestep_label.text.text = update_timestep_label(universe.usertime)
        self.current_actions = dict.fromkeys(['decrease_timestep','increase_timestep','prograde','retrograde','radialin','radialout','normal','antinormal','decrease_focus','increase_focus','spacecraft_focus','parent_focus','pause_timestep'],False)

        self.camera_background      = sprite_loader(camera, 'UI3_camera_normal'     ,-0.68  ,-1.01  ,0.43,self.background,batch=self.HUDBatch)
        self.spacecraft_background  = sprite_loader(camera, 'UI3_spacecraft_normal' ,-0.68  ,-1.01  ,0.43,self.background)
        self.parameters_background  = sprite_loader(camera, 'UI3_parameters_normal' ,-0.68  ,-1.015 ,0.43,self.background)

        self.time_background        = sprite_loader(camera, 'UI3_time_normal'       ,-1.02  ,-1.01  ,0.43,self.midground,batch=self.HUDBatch)
        self.time_center            = sprite_loader(camera, 'UI3_time_center'       ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_right             = sprite_loader(camera, 'UI3_time_right'        ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_rightR            = sprite_loader(camera, 'UI3_time_rightR'       ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_left              = sprite_loader(camera, 'UI3_time_left'         ,-1.02  ,-1.01  ,0.43,self.midground)
        self.time_leftR             = sprite_loader(camera, 'UI3_time_leftR'        ,-1.02  ,-1.01  ,0.43,self.midground)

        # Camera menu
        self.focus_left             = sprite_loader(camera, 'UI3_camera_left'       ,-0.68  ,-1.02  ,0.43,self.background)
        self.focus_right            = sprite_loader(camera, 'UI3_camera_right'      ,-0.68  ,-1.02  ,0.43,self.background)
        self.focus_spacecraft       = sprite_loader(camera, 'UI3_camera_spacecraft' ,-0.68  ,-1.01  ,0.43,self.background)
        self.focus_parent           = sprite_loader(camera, 'UI3_camera_parent'     ,-0.68  ,-1.01  ,0.43,self.background)

        # Spacecraft menu
        self.spacecraft_red         = sprite_loader(camera, 'UI3_spacecraft_red'        ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_prograde    = sprite_loader(camera, 'UI3_spacecraft_prograde'   ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_retrograde  = sprite_loader(camera, 'UI3_spacecraft_retrograde' ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_radialout   = sprite_loader(camera, 'UI3_spacecraft_radialout'  ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_radialin    = sprite_loader(camera, 'UI3_spacecraft_radialin'   ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_Pnormal     = sprite_loader(camera, 'UI3_spacecraft_Pnormal'    ,-0.68  ,-1.01  ,0.43,self.background)
        self.spacecraft_antinormal  = sprite_loader(camera, 'UI3_spacecraft_antinormal' ,-0.68  ,-1.01  ,0.43,self.background)

        # Parameters menu
        self.parameters_vessel      = sprite_loader(camera, 'UI3_parameters_vessel' ,-0.68  ,-1.015 ,0.43,self.background)
        self.name_label             = DataLabel(camera  ,-0.430 ,-0.743 ,self.ParameterBatch,self.foreground)
        self.primary_label          = DataLabel(camera  ,-0.430 ,-0.783 ,self.ParameterBatch,self.foreground)
        self.mass_label             = DataLabel(camera  ,-0.430 ,-0.822 ,self.ParameterBatch,self.foreground)
        self.radius_label           = DataLabel(camera  ,-0.430 ,-0.862 ,self.ParameterBatch,self.foreground)
        self.hill_label             = DataLabel(camera  ,-0.430 ,-0.901 ,self.ParameterBatch,self.foreground)
        self.SOI_label              = DataLabel(camera  ,-0.430 ,-0.941 ,self.ParameterBatch,self.foreground)
        self.axis_label             = DataLabel(camera  ,0.100  ,-0.743 ,self.ParameterBatch,self.foreground)
        self.eccentricity_label     = DataLabel(camera  ,0.100  ,-0.783 ,self.ParameterBatch,self.foreground)
        self.inclination_label      = DataLabel(camera  ,0.100  ,-0.822 ,self.ParameterBatch,self.foreground)
        self.long_label             = DataLabel(camera  ,0.100  ,-0.862 ,self.ParameterBatch,self.foreground)
        self.arg_label              = DataLabel(camera  ,0.100  ,-0.901 ,self.ParameterBatch,self.foreground)
        self.true_label             = DataLabel(camera  ,0.100  ,-0.941 ,self.ParameterBatch,self.foreground)
        self.apo_label              = DataLabel(camera  ,0.520  ,-0.743 ,self.ParameterBatch,self.foreground)
        self.peri_label             = DataLabel(camera  ,0.520  ,-0.783 ,self.ParameterBatch,self.foreground)
        self.period_label           = DataLabel(camera  ,0.520  ,-0.822 ,self.ParameterBatch,self.foreground)
        self.distance_label         = DataLabel(camera  ,0.520  ,-0.862 ,self.ParameterBatch,self.foreground)
        self.velocity_label         = DataLabel(camera  ,0.520  ,-0.901 ,self.ParameterBatch,self.foreground)

    def draw(self, universe, camera):
        glEnable(GL_DEPTH_TEST)
        self.TextBatch.draw()
        self.time_draw(universe, camera)
        self.draw_mode(universe, camera)
        self.HUDBatch.draw()
        glDisable(GL_DEPTH_TEST)

    def press_interaction(self, camera, x, y, button, modifiers):
        #print(x,y)
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
            self.parameters_setup(self.universe)

    def camera_control(self, camera, x, y, button, modifiers):
        if x > 0.23 and x < 0.4 and y > -0.91 and y < -0.79:
            if not camera.switch:
                camera.cinematic_view = True
                update_zoom(self.universe, camera, 1)
            camera.switch = False
        elif x > 0.46 and x < 0.525:
            self.current_actions['decrease_focus'] = True
            update_focus(self.universe, camera, -1)
        elif x > 0.63 and x < 0.69:
            self.current_actions['increase_focus'] = True
            update_focus(self.universe, camera, 1)
        elif x > 0.525 and x < 0.63 and y > -0.825:
            self.current_actions['spacecraft_focus'] = True
            update_focus(self.universe, camera, 0, self.universe.vessels[0])
        elif x > 0.525 and x < 0.63 and y < -0.825 and y > -0.913:
            self.current_actions['parent_focus'] = True
            update_focus(self.universe, camera, 0, self.universe.vessels[0].primary.object)
        elif x > 0.525 and x < 0.63 and y < -0.913:
            update_focus(self.universe, camera, 0, self.universe.star)

    def spacecraft_control(self, camera, x, y, button, modifiers):
        if x < -0.59:
            pass
        elif x < -0.552:
            self.current_actions['retrograde'] = True
        elif x < -0.507:
            self.current_actions['prograde'] = True
        elif x < -0.465:
            self.current_actions['radialin'] = True
        elif x < -0.419:
            self.current_actions['radialout'] = True
        elif x < -0.378:
            self.current_actions['antinormal'] = True
        elif x < -0.333:
            self.current_actions['normal'] = True

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
        if True in self.current_actions.values():
            if self.current_actions['decrease_focus']:
                self.focus_left.draw()
            elif self.current_actions['increase_focus']:
                self.focus_right.draw()
            elif self.current_actions['spacecraft_focus']:
                self.focus_spacecraft.draw()
            elif self.current_actions['parent_focus']:
                self.focus_parent.draw()

    def spacecraft_draw(self, universe, camera):
        if True in self.current_actions.values():
            if self.current_actions['prograde']:
                prograde(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)
                self.spacecraft_prograde.draw()
            elif self.current_actions['retrograde']:
                prograde(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
                self.spacecraft_retrograde.draw()
            elif self.current_actions['normal']:
                normal(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)
                self.spacecraft_Pnormal.draw()
            elif self.current_actions['antinormal']:
                normal(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
                self.spacecraft_antinormal.draw()
            elif self.current_actions['radialin']:
                radial(self.universe, self.universe.vessels[0], -self.universe.g*self.universe.timestep)
                self.spacecraft_radialin.draw()
            elif self.current_actions['radialout']:
                radial(self.universe, self.universe.vessels[0], self.universe.g*self.universe.timestep)
                self.spacecraft_radialout.draw()
        elif universe.usertime > 60:
            self.spacecraft_red.draw()

    def parameters_setup(self, universe):
        self.target = universe.focus_entity
        self.name_label.text.text          = self.target.name.rjust(14)
        self.primary_label.text.text       = self.target.primary.object.name.rjust(14)
        if isinstance(universe.focus_entity, Body):
            self.parameters_background.batch = self.HUDBatch
            self.parameters_vessel.batch = None
            self.mass_label.text.text      = format_numeric_label(self.target.bodycentre.mass)
            self.radius_label.text.text    = format_numeric_label(self.target.mean_radius)
            self.hill_label.text.text      = format_numeric_label(self.target.hill)
            self.SOI_label.text.text       = format_numeric_label(self.target.SOI)
        else:
            self.parameters_vessel.batch = self.HUDBatch
            self.parameters_background.batch = None

    def parameters_draw(self, universe, camera):
        if universe.focus_entity is not self.target:
            self.parameters_setup(universe)
        if universe.focus_entity.isvessel:
            self.mass_label.text.text      = format_numeric_label(self.target.orbit.rel_dist - self.target.primary.object.mean_radius)
            self.radius_label.text.text    = 'horizontal velocity'
            self.hill_label.text.text      = 'vertical velocity'
            self.SOI_label.text.text       = 'Barycentre' if isinstance(self.target.primary, Barycentre) else 'Bodycentre'
            self.apo_label.text.text           = format_numeric_label(self.target.orbit.semi_major_axis*(1+self.target.orbit.eccentricity) - self.target.primary.object.mean_radius)
            self.peri_label.text.text          = format_numeric_label(self.target.orbit.periapsis - self.target.primary.object.mean_radius)
        else:
            self.apo_label.text.text           = format_numeric_label(self.target.orbit.semi_major_axis*(1+self.target.orbit.eccentricity))
            self.peri_label.text.text          = format_numeric_label(self.target.orbit.periapsis)
        self.axis_label.text.text              = format_numeric_label(self.target.orbit.semi_major_axis)
        self.eccentricity_label.text.text      = format_numeric_label(self.target.orbit.eccentricity)
        self.inclination_label.text.text       = format_numeric_label(np.rad2deg(self.target.orbit.inclination))
        self.long_label.text.text              = format_numeric_label(np.rad2deg(self.target.orbit.long_ascending))
        self.arg_label.text.text               = format_numeric_label(np.rad2deg(self.target.orbit.arg_periapsis))
        self.true_label.text.text              = format_numeric_label(np.rad2deg(self.target.orbit.true_anomaly))
        self.period_label.text.text            = format_numeric_label(self.target.orbit.period)
        self.distance_label.text.text          = format_numeric_label(np.linalg.norm(self.target.orbit.rel_dist))
        self.velocity_label.text.text          = format_numeric_label(np.linalg.norm(self.target.barycentre.rvel))
        self.ParameterBatch.draw()

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

def format_numeric_label(value):
    magnitude = np.floor(np.log10(value))
    if magnitude > -4 and magnitude < 6:
        return('{:.8f}'.format(round(value, 8)).rjust(14))
    else:
        return ('%.4E' % Decimal(str(value))).rjust(14)



#self.sprite = pyglet.sprite.Sprite(pyglet.resource.animation('data/sprites/catjam.gif'), x=camera.halfwidth*-1, y=camera.halfheight*0.5)
