class Target:
    def __init__(self, entity):
        self.entity = entity
        self.flyby = False
        self.landing = False
        self.lim_time = False
        self.lim_dv = False
        self.orbit = False

'''
Include an orbit class, a data structure for grouping orbital elements and derived values.
This not only can be used to keep track of a current orbit but to specify a target orbit too.
'''

def GO1(universe, spacecraft, target, mode):
    '''
    Function GO1
        A generalised patched-conic approach to

    Inputs
    * Mode - indicates

    Outputs

    '''
