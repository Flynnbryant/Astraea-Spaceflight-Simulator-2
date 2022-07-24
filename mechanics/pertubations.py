import time
import numpy as np
from mechanics.orbit import *
from mechanics.centres import *
from spacecraft.vessel import *

def perturbations(universe):
    ''' loop through all bodies and vessels, applying pertubations if the timestep is sufficiently small to be more accurate than not considering them '''
    for entity in universe.entities[1:]:
        if universe.timestep < 0.02*entity.orbit.period:
            pass
            ''' 1. Correct for parent error '''

            ''' 2. Gravity Harmonics '''

            ''' 3. Pertubations from grandparent '''

            ''' 4. Pertubations from notable siblings '''

            ''' 5. Pertubations from notable piblings '''

            ''' 6. Pertubations from notable niblings '''

            ''' 7. General Relativity '''

    universe.profile.add('per')

def major_iblings(entity):
    entity.major_siblings = []
    entity.major_piblings = []
    entity.major_niblings = []
    for sibling in entity.primary.object.satellites:
        if sibling is not entity and sibling.barycentre.mass > 1e20:
            entity.major_siblings.append(sibling)

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
