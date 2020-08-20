from sympy import Point, Line
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


def cosine_law(a, b, c):
    return np.rad2deg(np.arccos(float((a**2 + b**2 - c**2) / (2 * a * b))))


# Constants
stroke_length = 120.  # mm
force_cylinder = 80.28  # N
point_F = Point(0, -160)
point_D = Point(-100, -5)

# Link lengths
length_BF = 140.  # mm
length_AB = 40.  # mm

finger_positions = np.arange(-70, 70, 1)
link_lengths = np.arange(1, 60, 1)

data = np.zeros((len(finger_positions), len(link_lengths)), np.float)


for i, finger_position in enumerate(finger_positions):
    # Define point A (the finger position)
    point_A = Point(finger_position, 0)

    # Find virtual link length AF
    length_AF = point_A.distance(point_F).evalf()

    # Solve for angle a1
    angle_a1 = np.rad2deg(np.arcsin(float(abs(point_A.x) / length_AF)))

    # Solve for angle a2
    angle_a2 = np.rad2deg(np.arccos(float((length_AF**2 + length_AB**2 - length_BF**2) / (2 * length_AB * length_AF))))
    angle_a2_test = cosine_law(length_AB, length_AF, length_BF)

    # Solve for angle f1
    angle_f1 = np.rad2deg(np.arcsin(float(abs(point_F.y) / length_AF)))

    # Solve for angle f2
    angle_f2 = cosine_law(length_BF, length_AF, length_AB)

    # Solve for angle f3
    angle_f3 = 130 - angle_f2 - angle_f1

    # Test multiple radius arm lengths
    for j, length_CF in enumerate(link_lengths):

        # Resolve link CF into its components
        length_CF_x = np.cos(np.deg2rad(angle_f3) * length_CF)
        length_CF_y = np.sin(np.deg2rad(angle_f3) * length_CF)

        # Solve for the components of virtual link CD
        length_CD_x = point_F.x - point_D.x - length_CF_x
        length_CD_y = point_F.y - point_D.y - length_CF_y

        # Solve for angle c2
        angle_c2 = np.rad2deg(np.arctan(float(abs(length_CD_y) / abs(length_CF_x))))

        # Solve for angle c1
        angle_c1 = 180 - angle_f3 - angle_c2

        # Solve for applied force at C
        force_C = force_cylinder * np.cos(np.deg2rad(angle_c1))

        # Solve for the applied force at the finger
        force_A = np.cos(np.deg2rad(angle_a2)) * force_C * length_CF / length_AF

        data[i, j] = force_A


fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(link_lengths, finger_positions)

surf = ax.plot_surface(X, Y, data, cmap=cm.coolwarm)
ax.set_xlabel('Link Lengths (mm)')
ax.set_ylabel('Stroke (mm)')
ax.set_zlabel('Force at Finger (N)')

plt.show()

