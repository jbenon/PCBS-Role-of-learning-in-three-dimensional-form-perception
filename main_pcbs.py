import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from math import *

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

def compute_plane_normal_vector(angle_x, angle_y):
    angle_x = angle_x*pi/180
    angle_y = angle_y*pi/180
    vec = np.zeros(3)
    vec[0] = cos(angle_x)
    vec[1] = cos(angle_y)
    vec[2] = sin(angle_y)
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

def project_structure_on_2d_plane(structure_3d, angle_x, angle_y):
    """
    Aggregates all the functions above.
    """
    
    normal_vec = compute_plane_normal_vector(angle_x, angle_y)
    structure_proj = project_3d_structure_on_3d_plane(structure_3d, normal_vec)
    basis = create_basis_to_extract_2d_coords_from_3d_plane(structure_proj, normal_vec)
    transf_matrix = compute_transformation_matrix_from_basis(basis)
    points_2d = extract_2d_coords_from_projected_structure(structure_proj, transf_matrix)
    return ([points_2d[:,0], points_2d[:,1]], structure_proj, normal_vec)
    

## test

nb_points = 7

structure_3d = generate_random_3d_structure(nb_points)
show_3d_structure(structure_3d)

plt.figure()

for i, angle_x in enumerate(np.arange(0, 181, 22.5)):
    (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d, angle_x, 0)
    plt.subplot(3, 3, i+1)
    plt.plot(points_2d[0], points_2d[1])
    plt.xlabel(f'Angle x = {angle_x}°')
    plt.xticks([])
    plt.yticks([])
    
plt.tight_layout()
plt.show()

## animation

nb_points = 7
nb_steps = 20
dt = 0.1
step_angle_x = 5
step_angle_y = 0

structure_3d = generate_random_3d_structure(nb_points)

all_points = []
all_structures = []
all_normal_vec = []

for i in range(nb_steps):
    angle_x = step_angle_x*i
    angle_y = step_angle_y*i
    (points_2d, structure_proj, normal_vec) = project_structure_on_2d_plane(structure_3d,angle_x, 0)
    all_points.append(points_2d)
    all_structures.append(structure_proj)
    all_normal_vec.append(normal_vec)
all_points = np.array(all_points)
all_structures = np.array(all_structures)
all_normal_vec = np.array(all_normal_vec)


fig = plt.figure()

mesh = np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))

ax3d = fig.add_subplot(121, projection='3d')
ax2d = fig.add_subplot(122)

def return_plane_coordinates(mesh, structure_proj, normal_vec):
    point = structure_proj[0]
    a, b, c = normal_vec[0], normal_vec[1], normal_vec[2]
    if a!= 0:
        Y = mesh[0]
        Z = mesh[1]
        X = (np.dot(point, normal_vec) - b*Y - c*Z)/a
    elif b!=0:
        X = mesh[0]
        Z = mesh[1]
        Y = (np.dot(point, normal_vec) - a*X - c*Z)/b
    else:
        X = mesh[0]
        Y = mesh[1]
        Z = (np.dot(point, normal_vec) - a*X - b*Y)/c
    return np.array([X, Y, Z])

for i in range(nb_steps):
    [X, Y, Z] = return_plane_coordinates(mesh, all_structures[i], all_normal_vec[i])
    if i==0:
        ax3d.plot(structure_3d[:, 0], structure_3d[:, 1], structure_3d[:, 2], c='k', linewidth=2)
        ax3d.plot_surface(X, Y, Z, alpha=0.5)
        line, = ax2d.plot(all_points[i][0], all_points[i][1])
        min = np.min(all_points)
        max = np.max(all_points)
        ax2d.set_xlim(min, max)
        ax2d.set_ylim(min, max)
        ax2d.set_xticks([])
        ax2d.set_yticks([])
    else:
        line.set_data(all_points[i][0], all_points[i][1])
        ax3d.clear()
        ax3d.plot(structure_3d[:, 0], structure_3d[:, 1], structure_3d[:, 2], c='k', linewidth=2)
        ax3d.plot_surface(X, Y, Z, alpha=0.5)
    plt.pause(dt)

plt.show()
