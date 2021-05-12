import sys
# Used to import the modules : relative paths in Python do not work on my computer.
sys.path.append('D:/Documents/Cogmaster/M1S2/PCBS/project/')

from custom_functions import *


## Parameters

nb_items = 5
nb_points = 12
beta = 45
alpha_step = 20
max_angle = 360


## Start experiment

np.random.seed(42)

set_A = []
set_B = []

for i in range(nb_items):
    set_A.append(generate_random_3d_structure(nb_points))
    set_B.append(generate_random_3d_structure(nb_points))

exp = design.Experiment(name="First experiment")
control.initialize(exp)
screen_x, screen_y = exp.screen.size

## Load stimuli

list_blocks_setA = []
list_blocks_setB = []
for structure_3d in set_A:
    list_blocks_setA.append(create_block_one_3d_structure(structure_3d, beta, alpha_step, min_angle, max_angle, repeat, screen_x, screen_y))
for structure_3d in set_B:
    list_blocks_setB.append(create_block_one_3d_structure(structure_3d, beta, alpha_step, min_angle, max_angle, repeat, screen_x, screen_y))
question = stimuli.TextLine(text="Did the object look rigid?", position = (0, 0))
yes = stimuli.TextLine(text="◄ Yes", position = (-50, -40))
no = stimuli.TextLine(text="No ►", position = (50, -40))
pause = stimuli.TextLine(text="Pause")

## Launch experiment
control.start(exp)
group = exp.subject % 3

if group == 0:
    # First group : set A / set B
    for training_block in list_blocks_setA:
        key, rt = display_block(exp, training_block, (question, yes, no))
        exp.data.add([group, 'train', 'A', training_block.id, key, rt])
    canvas = stimuli.BlankScreen()
    pause.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for testing_block in list_blocks_setB:
        key, rt = display_block(exp, testing_block, (question, yes, no))
        exp.data.add([group, 'test', 'B', training_block.id, key, rt])

elif group == 1:
    # Second group : set A or set B
    choice = np.random.binomial(1, 0.5)
    if choice:
        for testing_block in list_blocks_setA:
            key, rt = display_block(exp, testing_block, (question, yes, no))
            exp.data.add([group, 'test', 'A', training_block.id, key, rt])
    else:
        for testing_block in list_blocks_setB:
            key, rt = display_block(exp, testing_block, (question, yes, no))
            exp.data.add([group, 'test', 'B', training_block.id, key, rt])

else:
    # Third group : set B / set A
    for training_block in list_blocks_setB:
        key, rt = display_block(exp, training_block, (question, yes, no))
        exp.data.add([group, 'test', 'B', training_block.id, key, rt])
    canvas = stimuli.BlankScreen()
    pause.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for testing_block in list_blocks_setA:
        key, rt = display_block(exp, testing_block, (question, yes, no))
        exp.data.add([group, 'train', 'B', training_block.id, key, rt])
    
control.end()
