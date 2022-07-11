import time
import numpy as np
from OpenGL.GL import *
from mechanics.orbit import *
from numba import njit

#@njit
#def faster_calculate_trace(eccentricity, trace_detail, rotation_matrix, semi_major_axis, semi_minor_axis, periapsis):


class Trace:
    def __init__(self, entity, bodylength, vesseltype):
        self.entity = entity
        self.orbit = entity.orbit
        self.trace_detail = 512
        self.bodylength = bodylength
        self.bodytype = not vesseltype
        self.calculate_trace()

    def calculate_trace(self):
        if self.orbit.eccentricity < 1:
            values = np.linspace(0, 2*np.pi, self.trace_detail, dtype=np.float32)
            array = np.add(-0.5*self.orbit.eccentricity*np.sin(2*values),values)
            self.points = np.dot(self.orbit.rotation_matrix, np.array([
                self.orbit.semi_major_axis * np.cos(array) - self.orbit.semi_major_axis + self.orbit.periapsis,
                self.orbit.semi_minor_axis * np.sin(array)], dtype=np.float32))

    def update_trace(self):
        return np.array(self.points+self.entity.primary.apos[:, None]).T

    def draw(self, universe, camera):
        camera.moveCamera()
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLineWidth(1)
        glColor3f(*(self.entity.colorsmall*self.entity.specific_strength))
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_DOUBLE, 0, self.update_trace())
        glDrawArrays(GL_LINE_STRIP, 0, self.trace_detail)
        glDisableClientState(GL_VERTEX_ARRAY)
