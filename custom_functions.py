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

def compute_plane_normal_vector(angle_xy, angle_yz):
    angle_xy = angle_xy*pi/180
    angle_yz = angle_yz*pi/180
    vec = np.zeros(3)
    vec[0] = sin(angle_xy)*cos(angle_yz)
    vec[1] = sin(angle_xy)*cos(angle_yz)
    vec[2] = cos(angle_yz)
    return(normalize_vector(vec))


def project_3d_structure_on_3d_plane(structure_3d, normal_vec):
    structure_proj = []
    for point in structure_3d :
        point_proj = point - np.dot(point, normal_vec)*normal_vec
        structure_proj.append(point_proj)
    return np.array(structure_proj)

def create_basis_to_extract_2d_coords_from_3d_plane(structure_proj, normal_vec):
    A, B = structure_proj[0], structure_proj[1]
    U = normalize_vector(B-A)
    V = np.cross(U,normal_vec)
    basis = np.array([A, A+U, A+V, A+normal_vec])
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

def project_structure_on_2d_plane(structure_3d, angle_xy, angle_yz):
    """
    Aggregates all the functions above.
    """
    normal_vec = compute_plane_normal_vector(angle_xy, angle_yz)
    structure_proj = project_3d_structure_on_3d_plane(structure_3d, normal_vec)
    basis = create_basis_to_extract_2d_coords_from_3d_plane(structure_proj, normal_vec)
    transf_matrix = compute_transformation_matrix_from_basis(basis)
    points_2d = extract_2d_coords_from_projected_structure(structure_proj, transf_matrix)
    return (np.array([points_2d[:,0], points_2d[:,1]]), structure_proj, normal_vec)
    
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

def angles_rocking_around_axis(angle_step, angle_central_axis):
    if angle_step[0]==0:
        nb_angles = int(360//angle_step[1]+1)
        list_add_x = np.zeros(nb_angles)
        list_add_y = np.arange(0, 361, angle_step[1])[:nb_angles]
    elif angle_step[1]==0:
        nb_angles = int(360//angle_step[0]+1)
        list_add_y = np.zeros(nb_angles)
        list_add_x = np.arange(0, 361, angle_step[0])[:nb_angles]
    else:
        nb_angles = int(min(360//angle_step[0], 360//angle_step[1])+1)
        list_add_x = np.arange(0, 361, angle_step[0])[:nb_angles]
        list_add_y = np.arange(0, 361, angle_step[1])[:nb_angles]
    list_angle_xy = np.array(list_add_x+angle_central_axis[0])
    list_angle_yz = np.array(list_add_y+angle_central_axis[1])
    print(list_angle_xy, list_angle_yz)
    return (list_angle_xy, list_angle_yz)

def return_2d_structure_for_all_angles(structure_3d, list_angle_xy, list_angle_yz):
    all_points = []
    all_structures = []
    all_normal_vec = []
    for i, angle_yz in enumerate(list_angle_yz):
        angle_xy = list_angle_xy[i]
        (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d, angle_xy, angle_yz)
        all_points.append(points_2d)
        all_structures.append(structure_proj)
        all_normal_vec.append(normal_vec)
    all_points = np.array(all_points)
    all_structures = np.array(all_structures)
    all_normal_vec = np.array(all_normal_vec)
    return [all_points, all_structures, all_normal_vec]

def create_block_one_figure(structure_3d, angle_central_axis, angle_step, screen_x, screen_y):
    # Generates all the 2D views
    list_angle_xy, list_angle_yz = angles_rocking_around_axis(angle_step, angle_central_axis)
    [all_points, _, _] = return_2d_structure_for_all_angles(structure_3d, list_angle_xy, list_angle_yz)
    sidelength = min(screen_x, screen_y)-20
    all_x = normalize_list(all_points[:, 0, :], -sidelength//2, sidelength//2)
    all_y = normalize_list(all_points[:, 1, :], -sidelength//2, sidelength//2)
    # Aggregate them in the block
    block = design.Block()
    for i, angle_yz in enumerate(list_angle_yz):
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
# for i, angle_xy in enumerate(np.arange(0, 181, 22.5)):
#     (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d, angle_xy, 0)
#     plt.subplot(3, 3, i+1)
#     plt.plot(points_2d[0], points_2d[1])
#     plt.xlabel(f'Angle x = {angle_xy}°')
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
# step_angle_xy = 5
# step_angle_yz = 0
# 
# structure_3d = generate_random_3d_structure(nb_points)
# 
# all_points = []
# all_structures = []
# all_normal_vec = []
# 
# for i in range(nb_steps):
#     angle_xy = step_angle_xy*i
#     angle_yz = step_angle_yz*i
#     (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d,angle_xy, 0)
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
