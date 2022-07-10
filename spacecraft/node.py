import numpy as np

def sort_node(new, nodes):
    for existing_index, node in enumerate(nodes):
        if new.time < node.time:
            nodes.insert[existing_index, new]
            break
    return nodes

class Node:
    def __init__(self, vessel, time):
        self.vessel = vessel
        self.time = time

class Plan(Node):
    def __init__(self, vessel, time, data):
        super().__init__(vessel, time)
        self.data = data

    def run(universe):
        pass

class Maneuver(Node):
    def __init__(self, vessel, time, prograde, normal, radial):
        super().__init__(vessel, time)
        self.prograde = prograde
        self.normal = normal
        self.radial = radial

    def run(universe):
        prograde(universe, self.vessel, self.prograde)
        normal(universe, self.vessel, self.normal)
        radial(universe, self.vessel, self.radial)

def prograde(universe, vessel, value):
    vessel.barycentre.pvel += value*(vessel.bodycentre.rvel/np.linalg.norm(vessel.bodycentre.rvel))

def normal(universe, vessel, value):
    normalVec = np.cross(vessel.bodycentre.rpos, vessel.bodycentre.rvel)
    vessel.barycentre.pvel += value*(normalVec/np.linalg.norm(normalVec))

def radial(unvierse, vessel, value):
    normalVec = np.cross(vessel.bodycentre.rpos, vessel.bodycentre.rvel)
    radialVec = np.cross(vessel.bodycentre.rvel,normalVec)
    vessel.barycentre.pvel += value*(radialVec/np.linalg.norm(radialVec))
