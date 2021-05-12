"""
This script analyses the data outputed by exp1.py, and contained either in a folder given in argument, either in an example folder if there is no argument.
It displays two figures and saves them.
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
import numpy as np
import os


## Load and organize data

# Going through the data folder to collect each subject's data
if len(sys.argv)>1 :
    folder = sys.argv[1]+'/'
else:
    folder = 'example_data_exp1/'

answers_by_subject = [[[], []] for group in range(3)]
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    if os.path.isfile(file_path) and file[0:4]=='exp1':
        data_exp1 = pd.read_csv(file_path, comment='#')
        for block in range(0, len(data_exp1['subject_id']), 10):
            group = data_exp1['group'][block]
            set = int((data_exp1['set']=='B')[block])
            answers = data_exp1['looks_rigid'][block:block+9].to_numpy(dtype="object").astype(int)
            answers_by_subject[group][set].append(np.mean(answers))
answers_by_subject = np.array(answers_by_subject, dtype="object")

# Processing the answers by group and set
propor_rigid_by_group_and_set = [[0, 0] for group in range(3)]
std_rigid_by_group_and_set = [[0, 0] for group in range(3)]
for group in range(3):
    for set in range(2):
        if len(answers_by_subject[group,set])>0:
            propor_rigid_by_group_and_set[group][set] = np.mean(answers_by_subject[group,set])
            std_rigid_by_group_and_set[group][set] = np.std(answers_by_subject[group,set])
        else:
            propor_rigid_by_group_and_set[group][set] = 0
            std_rigid_by_group_and_set[group][set] = 0

# Processing the answers by train/test blocks
groups_and_sets_for_train_blocks = [(0,0), (2,1)]
groups_and_sets_for_test_blocks = [(0,1), (1,0), (1,1), (2,0)]
answers_train_blocks = []
answers_test_blocks = []
for (group, set) in groups_and_sets_for_train_blocks:
    answers_train_blocks.append(answers_by_subject[group,set])
for (group, set) in groups_and_sets_for_test_blocks:
    answers_test_blocks.append(answers_by_subject[group,set])

if len(answers_train_blocks[0])>0:
    propor_rigid_train_blocks = np.mean(answers_train_blocks[0])
    std_rigid_train_blocks = np.std(answers_train_blocks[0])
else:
    propor_rigid_train_blocks = 0
    std_rigid_train_blocks = 0
if len(answers_test_blocks[0])>0:
    propor_rigid_test_blocks = np.mean(answers_test_blocks[0])
    std_rigid_test_blocks = np.std(answers_test_blocks[0])
else:
    propor_rigid_test_blocks = 0
    std_rigid_test_blocks = 0

## Plot data

color_train = 'C0'
color_test = 'C1'

# Plot data by group and set
plt.close()
fig, ax = plt.subplots(1, 3, figsize=(12,7), sharey=True)
plt.subplots_adjust(left=0.06, right=0.99, bottom=0.05, top=0.9, wspace=0.2)
plt.suptitle('Answers by group and by set of images')
legend_elements = [Patch(facecolor=color_train, label='Training'), Patch(facecolor=color_test, label='Novel')]
for group in range(3):
    if group==0:
        color_bars = [color_train, color_test]
    elif group==1:
        color_bars = [color_test, color_test]
    else:
        color_bars = [color_test, color_train]
    ax[group].bar([1,2], propor_rigid_by_group_and_set[group], color=color_bars, tick_label=['Set A', 'Set B'], yerr = std_rigid_by_group_and_set[group], error_kw=dict(ecolor='grey'))
    ax[group].set_title(f'Group n°{group+1}')
    ax[group].set_ylim(0,1)
    ax[group].legend(handles=legend_elements, loc="upper center", ncol=1)
ax[0].set_ylabel('Proportion of structures judged rigid')
plt.savefig(folder[:-1]+'_answers_by_group_and_set.png')



# Plot data by train/test set
fig, ax = plt.subplots(1, 1, figsize=(7,5))
ax.bar([1,2], [propor_rigid_train_blocks, propor_rigid_test_blocks], color=[color_train, color_test], tick_label=['Training', 'Novel'], yerr=[std_rigid_train_blocks, std_rigid_test_blocks], error_kw=dict(ecolor='grey'))
ax.set_ylim(0,1)
plt.title('Answers by type of block')
plt.ylabel('Proportion of structures judged rigid')
plt.tight_layout()
if len(sys.argv)>2:
    plt.savefig(folder[:-1]+sys.argv[2]+'_answers_by_type_of_block.png')
else:
    plt.savefig(folder[:-1]+'_answers_by_type_of_block.png')

plt.show()