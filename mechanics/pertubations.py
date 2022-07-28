import time
import numpy as np
from mechanics.orbit import *
from mechanics.centres import *
from spacecraft.vessel import *

def perturbations(universe):
    ''' loop through all bodies and vessels, applying pertubations if the timestep is sufficiently small to be more accurate than not considering them '''
    for entity in universe.entities[1:]:
        ''' 1. Timestep stable precessions - Gravity Harmonics & General Relativity'''
        if entity.isvessel: # Keep this line in until nodal precession is in the correct reference frame.
            entity.orbit.nodal_precession = universe.timestep*entity.primary.object.precession_constant*np.cos(entity.orbit.inclination)/(entity.orbit.sqrta3omu*(entity.orbit.semi_major_axis*entity.orbit.omes)**2)

        if universe.timestep < 0.02*entity.orbit.period:
            ''' 2. Pertubations from notable siblings & parent '''
            if entity.barycentric:
                parent_error = 0.
                for sibling in entity.primary.satellites:
                    pass
                for sibling in entity.primary.object.bodycentre.satellites:
                    pass
            else:
                for sibling in entity.primary.object.barycentre.satellites:
                    pass
                for sibling in entity.primary.satellites:
                    pass

            ''' 3. Pertubations from grandparent '''
            if entity.primary.object.primary:
                grandparent_error = 0.

                ''' 4. Pertubations from notable piblings '''

            else:
                ''' 5. Pertubations from notable niblings '''
                pass

    universe.profile.add('per')

'''
# Barycentre
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


# Bodycentre
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
'''
