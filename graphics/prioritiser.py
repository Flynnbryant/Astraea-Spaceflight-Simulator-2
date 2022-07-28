from graphics.trace import *
from mechanics.body import *
from spacecraft.vessel import *
from analysis.profile import *
from graphics.labels import *
from graphics.scene import *

def update_zoom(universe, camera, modifier, focus_change=False):
    camera.camera_distance = np.clip(camera.camera_distance*modifier, universe.focus_entity.mean_radius*0.8, 1e13)
    camera.pos[2] = np.clip(-(camera.camera_distance*1e-15), -10, -0.0002)
    camera.inverse_scale_factor = np.clip((camera.camera_distance*1e4), 1e8, 2e15)
    camera.background.size = 50*camera.inverse_scale_factor
    camera.scale_factor = 1/camera.inverse_scale_factor
    if universe.focus_entity is universe.star:
        consistent = universe.focus_entity
        camera.planetary_view = False
    else:
        consistent = universe.focus_entity.local_planet
        camera.planetary_view = camera.camera_distance<consistent.hill
    global_strength = min(1,np.abs(1-camera.camera_distance/consistent.hill))

    if camera.planetary_view:
        consistent.spheroid.calculate_render_detail(universe, camera)
        for object in consistent.satellites:
            specific_strength(camera, universe, object, global_strength, planetary=True)
            object.spheroid.calculate_render_detail(universe, camera)
    else:
        for object in universe.star.satellites:
            specific_strength(camera, universe, object, global_strength, planetary=False)

    consistent.specific_strength = 1
    consistent.label.text.color = (*(consistent.color*consistent.specific_strength).astype(int), 255)

    update_features(universe, camera, focus_change)

def update_focus(universe, camera, modifier, target=False):
    if target:
        universe.focus_entity = target
        universe.focus = universe.focus_entity.focus_num
    else:
        universe.focus += modifier
        universe.focus_entity = universe.entities[universe.focus%(universe.entitylength)]
    universe.focus_entity.label.regenerate_label()
    update_zoom(universe,camera,1,focus_change = True)

def update_fov(universe, camera, modifier=1, value=None):
    if value:
        camera.fov = value
    camera.fov *= modifier
    update_zoom(universe, camera, 1)

def specific_strength(camera, universe, object, global_strength, planetary=True):
    # Planetary is an unused variable. When zoomed out to not be in planetary view, then switching focus between a planet and a moon causes a difference in specific strength of other sol satellites
    if object is universe.focus_entity:
        object.specific_strength = 1
    else:
        if object.primary.object is universe.focus_entity.primary.object:
            distance = max(universe.focus_entity.orbit.semi_major_axis,camera.camera_distance-object.orbit.semi_major_axis)
        else:
            distance = camera.camera_distance
        inner_strength = 2*distance/object.inner_label_distance - 1
        outer_strength = 2 - distance/object.outer_label_distance
        object.specific_strength = np.clip(min([inner_strength,outer_strength,global_strength]),0,1)
    object.label.text.color = (*(object.color*object.specific_strength).astype(int), 255)
