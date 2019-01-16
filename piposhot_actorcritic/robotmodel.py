#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Code explanation"""

import numpy as np
import matplotlib.pyplot as plt

def final_position(x_ball_init=0, y_ball_init=0, z_ball_init=0, speed=10,
    hang=45, vang=0, x_final=2):
    x_speed = speed*np.cos(hang*np.pi/180)*np.cos(vang*np.pi/180)
    y_speed = speed*np.sin(vang*np.pi/180)
    z_speed = speed*np.sin(hang*np.pi/180)

    t_final = (x_final-x_ball_init)/x_speed
    y_final = y_ball_init + t_final*y_speed
    z_final = -1/2*g*t_final**2 + z_speed*t_final + z_ball_init

    return y_final, z_final

def approx(y=0,target_size=0.1):
    if y<0:
        if abs(y)%target_size >= target_size/2:
            y_approx = -(abs(y)-abs(y)%(target_size/2)+target_size/2)
        else:
            y_approx = -(abs(y)-abs(y)%target_size)
    else:
        if y%target_size >= target_size/2:
            y_approx = y-y%(target_size/2)+target_size/2
        else:
            y_approx = y-y%(target_size)
    return y_approx

# Target parameters
x_final = 2
target_size = 0.1
target_y = 0
target_z = 0.5

# World parameters
g = 9.81       # m.s^-2

# Ball parameters
m = 2.7e-3      # kg
r = 2e-2        # m
x_ball_init = 0
y_ball_init = 0
z_ball_init = 0
speed = 10       # m/s

Y = []
Z = []
Y_approx = []
Z_approx = []
for i in range(13,41,2):
    for j in range(-20,21,2):
        y,z = final_position(x_ball_init, y_ball_init, z_ball_init, speed, i, j, x_final)
        y_approx = approx(y, target_size)
        z_approx = approx(z, target_size)
        Y.append(y)
        Z.append(z)
        Y_approx.append(y_approx)
        Z_approx.append(z_approx)

# plot everything

plt.scatter(Y,Z)
for i in np.arange(-1-target_size/2,1+3*target_size/2,target_size):
    for j in np.arange(0-target_size/2,1+3*target_size/2,target_size):
        plt.vlines(i,0-target_size/2,1+target_size/2,colors="k")
        plt.hlines(j,-1-target_size/2,1+target_size/2,colors="k")
plt.axis("equal")

plt.scatter(Y_approx,Z_approx,color="r")
plt.show()
