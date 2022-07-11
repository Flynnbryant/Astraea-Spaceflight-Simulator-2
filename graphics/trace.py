import time
import numpy as np
from OpenGL.GL import *
from mechanics.orbit import *
from numba import njit

@njit
def faster_calculate_trace(eccentricity, trace_detail, semi_major_axis, semi_minor_axis, periapsis):
    values = np.linspace(0, 2*np.pi, trace_detail)
    array = np.add(-0.5*eccentricity*np.sin(2*values),values)
    return [semi_major_axis * np.cos(array) + (periapsis - semi_major_axis), semi_minor_axis * np.sin(array)]

@njit
def faster_update_trace(points, apos):
    return (points+np.reshape(apos, (-1,1))).T

class Trace:
    def __init__(self, entity, bodylength, vesseltype):
        self.entity = entity
        self.orbit = entity.orbit
        self.trace_detail = 512
        self.bodylength = bodylength
        self.bodytype = not vesseltype
        self.points = np.dot(self.orbit.rotation_matrix,faster_calculate_trace(self.orbit.eccentricity, self.trace_detail, self.orbit.semi_major_axis, self.orbit.semi_minor_axis, self.orbit.periapsis))

    def draw(self, universe, camera):
        camera.moveCamera()
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLineWidth(1)
        glColor3f(*(self.entity.colorsmall*self.entity.specific_strength))
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_DOUBLE, 0, faster_update_trace(self.points, self.entity.primary.apos))
        glDrawArrays(GL_LINE_STRIP, 0, self.trace_detail)
        glDisableClientState(GL_VERTEX_ARRAY)
