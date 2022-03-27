from pyglet import *
from OpenGL.GL import *
from graphics.camera import *
from graphics.trace import *
from graphics.labels import *
from graphics.rings import *
from interface.prioritiser import *
from graphics.lighting import *
from interface.utilities import *
import numpy as np
import time

def drawScene(universe, camera):
    if universe.refresh_object.trace in camera.traces:
        universe.refresh_object.trace.calculate_trace()
    subtract = -universe.focus_entity.bodycentre.apos
    for entity in universe.entities:
        entity.bodycentre.apos += subtract
        entity.barycentre.apos += subtract

    camera.window.clear()
    #glClear(GL_COLOR_BUFFER_BIT)
    #glClear(GL_DEPTH_BUFFER_BIT)
    #glClear(GL_STENCIL_BUFFER_BIT)
    [feature.draw(universe, camera) for feature in camera.draw_features]
    glFlush()

def update_features(universe, camera, focus_change = False):
    camera.spheroids = []
    camera.traces = []
    camera.labels = [DrawProfile('tra')]
    camera.draw_features = [camera.light, camera.flare, DrawProfile('lig')]
    if camera.planetary_view:
        for object in [universe.focus_entity.local_planet] + universe.focus_entity.local_planet.satellites:
            if object.specific_strength > 0:
                if object.render_detail > 4:
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
    camera.labels.append(DrawProfile('lar')) # Keep in mind that rings are part of labels
    camera.draw_features += camera.spheroids + camera.traces + camera.labels

    if focus_change:
        for trace in camera.traces:
            trace.calculate_trace()
