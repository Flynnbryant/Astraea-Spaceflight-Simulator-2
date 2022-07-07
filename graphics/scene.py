from pyglet import *
from OpenGL.GL import *
from graphics.camera import *
from data.loading import *
from graphics.trace import *
from graphics.labels import *
from graphics.rings import *
from graphics.prioritiser import *
from graphics.lighting import *
import numpy as np
import time

def drawScene(universe, camera):
    recentre_solar_system(universe, camera)
    camera.window.clear()
    [feature.draw(universe, camera) for feature in camera.draw_features]
    glFlush()

def recentre_solar_system(universe, camera):
    if universe.refresh_object.trace in camera.traces:
        universe.refresh_object.trace.calculate_trace()
        universe.refresh_object.label.regenerate_label()
    subtract = -universe.focus_entity.bodycentre.apos
    for entity in universe.entities:
        entity.bodycentre.apos += subtract
        entity.barycentre.apos += subtract

def update_features(universe, camera, focus_change = False):
    camera.spheroids = []
    camera.traces = []
    camera.labels = [DrawProfile('tra')]
    camera.draw_features = [camera.HUD, DrawProfile('hud'), camera.flare, camera.light, DrawProfile('lig')]
    if camera.planetary_view:
        for object in [universe.focus_entity.local_planet] + universe.focus_entity.local_planet.satellites:
            if object.specific_strength > 0:
                if object.spheroid.render_detail > 0:
                    camera.spheroids.append(object.spheroid)
                if object.rings:
                    camera.labels.append(object.rings)
                if not camera.cinematic_view:
                    camera.traces.append(object.trace)
                    camera.labels.append(object.label)

    else:
        for object in universe.star.satellites:
            if object.specific_strength > 0:
                camera.traces.append(object.trace)
                camera.labels.append(object.label)

    if not camera.cinematic_view:
        for vessel in universe.vessels:
            camera.labels.append(vessel.label)
            camera.traces.append(vessel.trace)
        camera.draw_features.append(camera.background)

    camera.spheroids.append(DrawProfile('sph'))
    #camera.labels.append(universe.focus_entity.local_planet.labelbatch)
    #camera.labels.append(universe.vessels[0].labelbatch)
    camera.labels.append(DrawProfile('lar')) # Keep in mind that rings are part of labels
    camera.draw_features += camera.spheroids + camera.traces + camera.labels

    if focus_change:
        for trace in camera.traces:
            trace.calculate_trace()
