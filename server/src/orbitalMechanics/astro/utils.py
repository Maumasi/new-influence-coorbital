import numpy as np


def modulo(x, y):
    return ((x % y) + y) % y



def rotation_matrix(angle, axis):
    # Create identity matrix
    R = np.eye(3)
    
    # Calculate sin and cos
    c = np.cos(angle)
    s = np.sin(angle)
    
    # Update the matrix elements based on the rotation axis
    if axis == 0:  # Rotation around the x-axis
        R[1, 1] = c
        R[1, 2] = -s
        R[2, 1] = s
        R[2, 2] = c
    elif axis == 1:  # Rotation around the y-axis
        R[0, 0] = c
        R[0, 2] = s
        R[2, 0] = -s
        R[2, 2] = c
    elif axis == 2:  # Rotation around the z-axis
        R[0, 0] = c
        R[0, 1] = -s
        R[1, 0] = s
        R[1, 1] = c
    
    return R
