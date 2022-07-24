import time
import numpy as np
from mechanics.orbit import *
from mechanics.centres import *
from spacecraft.vessel import *

def perturbations(universe):
    ''' loop through all bodies and vessels, applying pertubations if the timestep is sufficiently small to be more accurate than not considering them '''
    for entity in universe.entities[1:]:
        if universe.timestep < 0.02*entity.orbit.period:

            ''' 1. Correct for parent error '''
            #if entity.isbarycentric:
            if isinstance(entity.primary, Barycentre) and isinstance(entity, Vessel):
                true_vec = entity.primary.object.bodycentre.rpos-entity.barycentre.rpos
                entity.barycentre.pvel += universe.timestep*entity.primary.object.bodycentre.SGP*((true_vec/np.linalg.norm(true_vec)**3) + (entity.barycentre.rpos/np.linalg.norm(entity.barycentre.rpos)**3))

            ''' 2. Gravity Harmonics '''

            ''' 3. Pertubations from notable siblings '''

            ''' 4. Pertubations from grandparent '''
            if entity.primary.object.primary:
                grandparent_vec = entity.primary.object.barycentre.rpos + entity.barycentre.rpos #THIS IS INCORRECT FOR BODYCENTRE ORBITS. Check vector algebra taking into account parent bodycentre around parent barycentre.
                entity.barycentre.pvel += universe.timestep*entity.primary.object.PP_SGP*((-grandparent_vec/np.linalg.norm(grandparent_vec)**3) - (-entity.primary.object.barycentre.rpos/np.linalg.norm(entity.primary.object.barycentre.rpos)**3))

            ''' 5. Pertubations from notable piblings '''

            ''' 6. Pertubations from notable niblings '''

            ''' 7. General Relativity '''

    universe.profile.add('per')

def major_siblings(entity):
    major_siblings = []
    for sibling in entity.primary.object.satellites:
        if sibling is not entity and sibling.barycentre.mass > 1e20:
            major_siblings.append(sibling)
    return major_siblings

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
