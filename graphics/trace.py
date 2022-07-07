import time
import numpy as np
from OpenGL.GL import *
from mechanics.orbit import *

class Trace:
    def __init__(self, entity, bodylength, vesseltype):
        self.entity = entity
        self.trace_detail = 512
        self.bodylength = bodylength
        self.bodytype = not vesseltype
        self.calculate_trace()

    def calculate_trace(self):
        if self.entity.eccentricity < 1:
            values = np.linspace(0, 2*np.pi, self.trace_detail, dtype=np.float32)
            array = np.add(-0.5*self.entity.eccentricity*np.sin(2*values),values)
            self.points = np.matmul(self.entity.rotation_matrix, np.array([
                self.entity.semi_major_axis * np.cos(array) - self.entity.semi_major_axis + self.entity.periapsis,
                self.entity.semi_minor_axis * np.sin(array)], dtype=np.float32))

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
