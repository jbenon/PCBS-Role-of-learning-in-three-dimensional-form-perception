"""
This script recreates an illusion evoked by Sinha and Poggio (1996).
It should display a walking man in 2D, which is in fact a rotating 3D structure.
"""


from custom_functions import *

## Parameters

BETA = 0
ALPHA_STEP = 5
MIN_ANGLE = -45
MAX_ANGLE = 45
REPEAT = True

## Start experiment

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
walking_man_3d[:,1], walking_man_3d[:,2] = np.copy(walking_man_3d[:,2]), -np.copy(walking_man_3d[:,1])
exp2 = design.Experiment(name="Illusion")
control.initialize(exp2)
screen_x, screen_y = exp2.screen.size


## Load stimuli

block = create_block_one_3d_structure(walking_man_3d, BETA, ALPHA_STEP, MIN_ANGLE, MAX_ANGLE, REPEAT, screen_x, screen_y, structure_width=0.2, structure_height=0.9)


## Launch experiment
control.start(exp2)
display_block(exp2, block, timestep=100)
control.end(exp2)