from graphics.trace import *
from mechanics.body import *
from spacecraft.vessel import *
from analysis.profile import *
from graphics.labels import *
from interface.utilities import *
from graphics.scene import *

def update_zoom(universe, camera, modifier, focus_change=False):
    camera.camera_distance = np.clip(camera.camera_distance*modifier, universe.focus_entity.mean_radius*0.8, 1e13)
    camera.pos[2] = np.clip(-(camera.camera_distance*1e-15), -10, -0.0002)
    camera.inverse_scale_factor = np.clip((camera.camera_distance*1e4), 1e8, 2e15)
    camera.background.size = 50*camera.inverse_scale_factor
    camera.scale_factor = 1/camera.inverse_scale_factor
    consistent = universe.focus_entity.local_planet
    global_strength = min(1,np.abs(1-camera.camera_distance/consistent.hill))
    camera.planetary_view = camera.camera_distance<consistent.hill

    if camera.planetary_view:
        render_detail(camera, universe, consistent)
        for object in consistent.satellites:
            specific_strength(camera, universe, object, global_strength)
            render_detail(camera, universe, object)
    else:
        for object in universe.star.satellites:
            specific_strength(camera, universe, object, global_strength)

    consistent.specific_strength = 1
    consistent.label.color = (*(consistent.color*consistent.specific_strength).astype(int), 255)

    update_features(universe, camera, focus_change)

def update_focus(universe, camera, modifier):
    if not camera.switch:
        camera.switch = True
        universe.focus += modifier
        universe.focus_entity = universe.entities[1+universe.focus%(universe.entitylength)]
        universe.focus_entity.label.regenerate_label()
        update_zoom(universe,camera,1,focus_change = True)

def update_fov(universe, camera, modifier=1, value=None):
    if value:
        camera.fov = value
    camera.fov *= modifier
    update_zoom(universe, camera, 1)
