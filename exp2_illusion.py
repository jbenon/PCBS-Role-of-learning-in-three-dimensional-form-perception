from custom_functions import *


## Parameters

beta = 0
alpha_step = 5
min_angle = 10
max_angle = 60
repeat = True

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

block = create_block_one_3d_structure(walking_man_3d, beta, alpha_step, min_angle, max_angle, repeat, screen_x, screen_y, structure_width=0.3, structure_height=0.9)


## Launch experiment
control.start(exp2)
display_block(exp2, block)
control.end(exp2)