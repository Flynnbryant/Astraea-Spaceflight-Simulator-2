import numpy as np
from mechanics.utilities import *

def create_centres(object, mass, grav_constant):
    SGP = mass*grav_constant
    return Bodycentre(object, mass, SGP), Barycentre(object, mass, SGP)

class Centre():
    def __init__(self, object, mass, SGP):
        self.apos = new_vector()
        self.rpos = new_vector()
        self.object = object
        self.satellites = []
        self.mass = mass
        self.inverse_mass = 1/mass
        self.SGP = SGP
        self.inverse_SGP = 1/SGP

class Barycentre(Centre):
    def __init__(self, object, mass, SGP):
        super().__init__(object, mass, SGP)
        self.ppos = new_vector()
        self.pvel = new_vector()

    def pv_vec(self, centre, sibling):
        return sibling.primary.bary_request_pv_vec(centre, sibling)

    def ps_vec(self, centre, sibling):
        return sibling.primary.bary_request_ps_vec(centre, sibling)

    def bary_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-centre.rpos

    def body_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-(centre.rpos+centre.object.primary.object.bodycentre.rpos)

    def bary_request_ps_vec(self, centre, sibling):
        return centre.rpos/np.linalg.norm(centre.rpos)**3

    def body_request_ps_vec(self, centre, sibling):
        return -sibling.barycentre.rpos/np.linalg.norm(sibling.barycentre.rpos)**3

    def check_model(self, universe, vessel):
        if vessel.periapsis < self.object.barycentre_transition:
            vessel.change_primary(universe, vessel.primary.object, barycentre=False)
        elif vessel.rel_dist > vessel.primary.object.SOI:
            vessel.change_primary(universe, vessel.primary.object.primary.object, barycentre=False)
        elif vessel.rel_dist < vessel.primary.object.mean_radius:
            vessel.collision(universe, vessel)

class Bodycentre(Centre):
    def __init__(self, object, mass, SGP):
        super().__init__(object ,mass, SGP)

    def pv_vec(self, centre, sibling):
        return sibling.primary.body_request_pv_vec(centre, sibling)

    def ps_vec(self, centre, sibling):
        return sibling.primary.body_request_ps_vec(centre, sibling)

    def bary_request_pv_vec(self, centre, sibling):
        return centre.object.primary.object.bodycentre.rpos + sibling.barycentre.rpos - centre.rpos

    def body_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-centre.rpos

    def bary_request_ps_vec(self, centre, sibling):
        return -centre.rpos/np.linalg.norm(centre.rpos)**3

    def body_request_ps_vec(self, centre, sibling):
        return 0.

    def check_model(self, universe, vessel):
        if vessel.periapsis > self.object.barycentre_transition:
            vessel.change_primary(universe, vessel.primary.object, barycentre=True)
        elif vessel.rel_dist < vessel.primary.object.mean_radius:
            vessel.collision(universe, vessel)
