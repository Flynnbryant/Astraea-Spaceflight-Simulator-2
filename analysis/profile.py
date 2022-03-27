''' profiler.py
A debugging feature to understand the use of processing time on each module. The
Profile class is first initialised in universe.py when the Universe class is
initialised. At certain points throughout the code, the module name and current
time is added to the profile.modules list as per: universe.profile.add('gravity')

Then at the end of each frame, astraea.py calls the print_profile function which
will calculate the total time spent on that frame, as well as the fraction of
that total time each module used up, and will print that information.
'''

import time
from statistics import mean
import numpy as np

class Profile():
    def __init__(self, display):
        self.display = display
        self.firstframe = time.time()
        self.frame_end = time.time()
        self.framecount = 0
        self.modules = []
        self.groups = {}
        self.moving_length = 200
        self.fpshistory = np.zeros(self.moving_length)
        self.mshistory = np.zeros(self.moving_length)
        self.outputend = 0
        self.colors = ['21','27','33','39','45','51','50','49','48','47','46','82','118','154','190','226','220','214','208','202','196']

    def add(self, name):
        self.modules.append([name, time.time()])

    def output(self, dt):
        if self.display:
            ''' display initialisation time '''
            if self.firstframe:
                print(time.time()-self.firstframe)
                self.firstframe = False

            ''' calculate and format fps '''
            totaltime = (time.time() - self.frame_end)
            fps = 1/totaltime
            ms = 1000*totaltime
            self.fpshistory[self.framecount%self.moving_length]=fps
            self.mshistory[self.framecount%self.moving_length]=ms
            total = f'\033[38;5;{self.colors[np.clip(int(ms*0.6),0,20)]}m'
            total += f'{str(round(mean(self.fpshistory))).rjust(3)}, '
            total += f'{str(round(fps)).rjust(3)} fps, time(ms) '
            total += f'{str(mean(self.mshistory))[0:4]}, '
            total += f'{str(ms)[0:4]} |'

            ''' convert timestamps to datapoints '''
            entrynum = self.framecount%self.moving_length
            for entry in self.modules:
                if entry[0] not in self.groups:
                    self.groups[entry[0]] = np.zeros(self.moving_length)
                self.groups[entry[0]][entrynum] = entry[1] - self.frame_end
                self.frame_end = entry[1]

            ''' calculate and display formatted means '''
            for name, value in self.groups.items():
                duration = 1000*(mean(value))
                total += f'\033[38;5;{self.colors[np.clip(int(20*duration),0,20)]}m {name} {str(duration)[0:4]},'

            ''' finish '''
            print(total)
            self.frame_end = time.time()
            self.framecount += 1
        self.modules = []

class DrawProfile():
    def __init__(self, name):
        self.name = name

    def draw(self, universe, camera):
        universe.profile.modules.append([self.name, time.time()])
