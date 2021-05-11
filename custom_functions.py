import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from math import *
import re
from expyriment import control, stimuli, io, design, misc

"""
Wow description
"""

## Generate the 3D structure

def generate_random_3d_structure(nb_points):
    structure = np.random.random_sample((nb_points, 3))
    return structure

def show_3d_structure(structure_3d):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(structure_3d[:, 0], structure_3d[:, 1], structure_3d[:, 2], c='k', linewidth=2)
    plt.show()

## Project on a 2D plane

def normalize_vector(vec):
    norm = np.linalg.norm(vec)
    if norm == 0: 
       return vec
    else:
        return vec/norm

def compute_plane_normal_vector(alpha, beta):
    alpha = np.radians(alpha)
    beta = np.radians(beta)
    vec = np.zeros(3)
    vec[0] = cos(alpha)*cos(beta)
    vec[1] = sin(alpha)*cos(beta)
    vec[2] = sin(beta)
    return(normalize_vector(vec))


def project_3d_structure_on_3d_plane(structure_3d, normal_vec):
    structure_proj = []
    for point in structure_3d :
        point_proj = point - np.dot(point, normal_vec)*normal_vec
        structure_proj.append(point_proj)
    return np.array(structure_proj)

def create_basis_to_extract_2d_coords_from_3d_plane(structure_proj, normal_vec, alpha):
    orig = np.zeros(3)
    U = normalize_vector(structure_proj[0])
    V = np.cross(U,normal_vec)
    basis = np.array([orig, orig+U, orig+V, orig+normal_vec])
    return basis

def compute_transformation_matrix_from_basis(basis):
    M1 = np.concatenate((basis.T, [np.ones(4)]), axis=0)
    M2 = np.array([[0,1,0,0], [0,0,1,0], [0,0,0,1], [1,1,1,1]])
    transf_matrix = np.dot(M2, np.linalg.inv(M1))
    return transf_matrix

def extract_2d_coords_from_projected_structure(structure_proj, transf_matrix):
    points_2d = []
    for point in structure_proj:
        point = np.concatenate((point, [1]))
        points_2d.append(np.dot(transf_matrix, point))
    return np.array(points_2d)

def project_structure_on_2d_plane(structure_3d, alpha, beta):
    """
    Aggregates all the functions above.
    """
    normal_vec = compute_plane_normal_vector(alpha, beta)
    structure_proj = project_3d_structure_on_3d_plane(structure_3d, normal_vec)
    basis = create_basis_to_extract_2d_coords_from_3d_plane(structure_proj, normal_vec, alpha)
    transf_matrix = compute_transformation_matrix_from_basis(basis)
    if beta==45 or (alpha >0 and alpha <=180):
        points_2d = extract_2d_coords_from_projected_structure(structure_proj, transf_matrix)
        points_array = np.array([points_2d[:,0], points_2d[:,1]])
    else:
        # To check: only change y coords ?
        # Also include beta in the condition
        points_2d = extract_2d_coords_from_projected_structure(structure_proj, transf_matrix)
        points_array = -np.array([points_2d[:,0], points_2d[:,1]])
    return (points_array, structure_proj, normal_vec)
    
## Display with experiment

def normalize_list(list, new_min, new_max):
    # Normalize between 0 and 1
    list = (list-np.min(list))/(np.max(list) - np.min(list))
    # Stretch
    list = (new_max-new_min)*list+new_min
    return list

def display_block(exp, block, present_text=None, timestep=200):
    for trial in block.trials:
        canvas = stimuli.BlankScreen()
        for stim in trial.stimuli:
            stim.plot(canvas)
        canvas.present()
        exp.clock.wait(timestep)
    if present_text is not None:
        canvas = stimuli.BlankScreen()
        for text in present_text:
            text.plot(canvas)
        canvas.present()
        key, rt = exp.keyboard.wait([misc.constants.K_LEFT,
                                        misc.constants.K_RIGHT])
        return (key, rt)
        
    

## Manipulate rotating figures

def angles_rocking_around_axis_z(beta, alpha_step, min_angle=0, max_angle=360):
    nb_steps = int((max_angle-min_angle)//alpha_step)
    list_alpha = [min_angle+i*alpha_step for i in range(nb_steps)]
    list_beta = [beta for i in range(nb_steps)]
    return (list_alpha, list_beta)

def return_2d_structure_for_all_angles(structure_3d, list_alpha, list_beta):
    all_points = []
    all_structures = []
    all_normal_vec = []
    for i, beta in enumerate(list_beta):
        alpha = list_alpha[i]
        (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d, alpha, beta)
        all_points.append(points_2d)
        all_structures.append(structure_proj)
        all_normal_vec.append(normal_vec)
    all_points = np.array(all_points)
    all_structures = np.array(all_structures)
    all_normal_vec = np.array(all_normal_vec)
    return [all_points, all_structures, all_normal_vec]

# Add parameter to change the normalization on the screen (for the exp2)
def create_block_one_figure(structure_3d, beta, alpha_step, screen_x, screen_y, min_angle, max_angle, structure_width=0.9, structure_height=0.9, repeat=False):
    # Generates all the 2D views
    list_alpha, list_beta = angles_rocking_around_axis_z(beta, alpha_step, min_angle, max_angle)
    if repeat:
        list_alpha = np.concatenate((list_alpha, np.flip(list_alpha, axis=0)), axis=0)
        list_beta = np.concatenate((list_beta, np.flip(list_beta, axis=0)), axis=0)
    [all_points, _, _] = return_2d_structure_for_all_angles(structure_3d, list_alpha, list_beta)
    structure_width = screen_x*structure_width
    structure_height = screen_y*structure_height
    all_x = normalize_list(all_points[:, 0, :], -structure_width//2, structure_width//2)
    all_y = normalize_list(all_points[:, 1, :], -structure_height//2, structure_height//2)
    # Aggregate them in the block
    block = design.Block()
    for i, beta in enumerate(list_beta):
        trial = design.Trial()
        # Add 2d figure to the trial
        for point in range(len(structure_3d)-1):
            point_start = (all_x[i, point], all_y[i, point])
            point_end = (all_x[i, point+1], all_y[i, point+1])
            stim = stimuli.Line(point_start, point_end, line_width=4)
            stim.preload()
            trial.add_stimulus(stim)
        block.add_trial(trial)
    return block

# ## test
# 
# nb_points = 7
# 
# structure_3d = generate_random_3d_structure(nb_points)
# show_3d_structure(structure_3d)
# 
# plt.figure()
# 
# for i, alpha in enumerate(np.arange(0, 181, 22.5)):
#     (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d, alpha, 0)
#     plt.subplot(3, 3, i+1)
#     plt.plot(points_2d[0], points_2d[1])
#     plt.xlabel(f'Angle x = {alpha}°')
#     plt.xticks([])
#     plt.yticks([])
#     
# plt.tight_layout()
# plt.show()
# 
# ## animation
# 
# nb_points = 7
# nb_steps = 100
# dt = 0.1
# step_alpha = 5
# step_beta = 0
# 
# structure_3d = generate_random_3d_structure(nb_points)
# 
# all_points = []
# all_structures = []
# all_normal_vec = []
# 
# for i in range(nb_steps):
#     alpha = step_alpha*i
#     beta = step_beta*i
#     (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d,alpha, 0)
#     all_points.append(points_2d)
#     all_structures.append(structure_proj)
#     all_normal_vec.append(normal_vec)
# all_points = np.array(all_points)
# all_structures = np.array(all_structures)
# all_normal_vec = np.array(all_normal_vec)
# 
# 
# fig = plt.figure()
# 
# mesh = np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))
# 
# ax3d = fig.add_subplot(121, projection='3d')
# ax3d.plot(structure_3d[:, 0], structure_3d[:, 1], structure_3d[:, 2], c='k', linewidth=2)
# ax2d = fig.add_subplot(122)
# 
# 
# for i in range(nb_steps):
#     if i==0:
#         line, = ax2d.plot(all_points[i][0], all_points[i][1])
#         min = np.min(all_points)
#         max = np.max(all_points)
#         ax2d.set_xlim(min, max)
#         ax2d.set_ylim(min, max)
#         ax2d.set_xticks([])
#         ax2d.set_yticks([])
#     else:
#         line.set_data(all_points[i][0], all_points[i][1])
#     plt.pause(dt)
# 
# plt.show()
