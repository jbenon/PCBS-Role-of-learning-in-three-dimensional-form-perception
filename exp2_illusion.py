import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from math import *
from expyriment import control, stimuli, io, design, misc

import sys
# Used to import the modules : relative paths in Python do not work on my computer.
sys.path.append('D:/Documents/Cogmaster/M1S2/PCBS/project/')

from custom_functions import *


## Experiment 2

# Parameters

angle_step = (22.5,0)
angle_central_axis = (0,90)


# Start experiment

walking_man_3d = np.array([
                [0, 0, -0.4],
                [3, 6, 1.1],
                [6,11,0],
                [8,6,1.4],
                [12,0,-0.1],
                [8,6,1.4],
                [6,11,0],
                [6,18,0],
                [6,19,0],
                [6,21,0.5],
                [6,19,0],
                [6,18,0],
                [4,14,-1],
                [3,10,0],
                [4,14,-1],
                [6,18,0],
                [8,14,-1],
                [9,10,0]])
walking_man_3d[:,0] = walking_man_3d[:,0] - 6*np.ones(len(walking_man_3d))
walking_man_3d[:,1], walking_man_3d[:,2] = walking_man_3d[:,2], walking_man_3d[:,1]
exp2 = design.Experiment(name="Illusion")
control.initialize(exp2)
screen_x, screen_y = exp2.screen.size

# Load stimuli
block = create_block_one_figure(walking_man_3d, angle_central_axis, angle_step, screen_x, screen_y)


# Launch experiment
control.start(exp2)
display_block(exp2, block)
control.end(exp2)