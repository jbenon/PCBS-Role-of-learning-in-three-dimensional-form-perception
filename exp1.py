"""
This script recreates the first experience from Sinha and Poggio (1996).
It saves the data from the experiment in two subfiles, data and event.
The data can then be analyzed with the script analyse_data_exp1.py.
"""


from custom_functions import *

## Parameters

NB_ITEMS = 10
NB_POINTS = 8
BETA = 45
ALPHA_STEP = 20
MIN_ANGLE = 0
MAX_ANGLE = 360
REPEAT = False

KEY_RIGID = misc.constants.K_LEFT
KEY_NONRIGID = misc.constants.K_RIGHT


## Start experiment

np.random.seed(42)

set_A = []
set_B = []

for i in range(NB_ITEMS):
    set_A.append(generate_random_3d_structure(NB_POINTS))
    set_B.append(generate_random_3d_structure(NB_POINTS))

exp = design.Experiment(name="First experiment")
control.initialize(exp)
screen_x, screen_y = exp.screen.size


## Load stimuli

list_blocks_setA = []
list_blocks_setB = []
for structure_3d in set_A:
    list_blocks_setA.append(create_block_one_3d_structure(structure_3d, BETA, ALPHA_STEP, MIN_ANGLE, MAX_ANGLE, REPEAT, screen_x, screen_y))
for structure_3d in set_B:
    list_blocks_setB.append(create_block_one_3d_structure(structure_3d, BETA, ALPHA_STEP, MIN_ANGLE, MAX_ANGLE, REPEAT, screen_x, screen_y))
intro = stimuli.TextLine(text="After each motion sequence, click on the left arrow to indicate that the shape looked rigid, and on the right arrow to indicate that it looked non-rigid.")
question = stimuli.TextLine(text="Did the object look rigid?", position = (0, 0))
yes = stimuli.TextLine(text="◄ Yes", position = (-50, -40))
no = stimuli.TextLine(text="No ►", position = (50, -40))
pause = stimuli.TextLine(text="Pause")


## Launch experiment

control.start(exp)
group = (exp.subject-1) % 3
exp.add_data_variable_names(["group", "type_of_block", "set", "looks_rigid", "rt"])

if group == 0:
    # First group : set A / set B
    canvas = stimuli.BlankScreen()
    intro.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for training_block in list_blocks_setA:
        key, rt = display_block(exp, training_block, (question, yes, no))
        exp.data.add([group, 'train', 'A', key==KEY_RIGID, rt])
    canvas = stimuli.BlankScreen()
    pause.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for testing_block in list_blocks_setB:
        key, rt = display_block(exp, testing_block, (question, yes, no))
        exp.data.add([group, 'test', 'B', key==KEY_RIGID, rt])

elif group == 1:
    # Second group : set A or set B
    choice = np.random.binomial(1, 0.5)
    canvas = stimuli.BlankScreen()
    intro.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    if choice:
        for testing_block in list_blocks_setA:
            key, rt = display_block(exp, testing_block, (question, yes, no))
            exp.data.add([group, 'test', 'A', key==KEY_RIGID, rt])
    else:
        for testing_block in list_blocks_setB:
            key, rt = display_block(exp, testing_block, (question, yes, no))
            exp.data.add([group, 'test', 'B', key==KEY_RIGID, rt])

else:
    # Third group : set B / set A
    canvas = stimuli.BlankScreen()
    intro.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for training_block in list_blocks_setB:
        key, rt = display_block(exp, training_block, (question, yes, no))
        exp.data.add([group, 'train', 'B', key==KEY_RIGID, rt])
    canvas = stimuli.BlankScreen()
    pause.plot(canvas)
    canvas.present()
    exp.clock.wait(5000)
    for testing_block in list_blocks_setA:
        key, rt = display_block(exp, testing_block, (question, yes, no))
        exp.data.add([group, 'test', 'A', key==KEY_RIGID, rt])
    
control.end()
