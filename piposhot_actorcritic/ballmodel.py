#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Code explanation"""

import numpy as np

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

def final_position(x_ball_init=0, y_ball_init=0, z_ball_init=0, speed=10,
    hang=45, vang=0, x_final=2,target_size=0.1):
    g = 9.81       # m.s^-2
    x_speed = speed*np.cos(hang*np.pi/180)*np.cos(vang*np.pi/180)
    y_speed = speed*np.sin(vang*np.pi/180)
    z_speed = speed*np.sin(hang*np.pi/180)

    t_final = (x_final-x_ball_init)/x_speed
    y_final = y_ball_init + t_final*y_speed
    z_final = -1/2*g*t_final**2 + z_speed*t_final + z_ball_init

    y_approx = int(approx(y_final, target_size)/target_size)
    z_approx = int(approx(z_final, target_size)/target_size)

    return y_approx, z_approx

def main():
    # Target parameters
    x_final = 2
    target_size = 0.1
    target_y = 0
    target_z = 0.5

    # World parameters

    # Ball parameters
    m = 2.7e-3      # kg
    r = 2e-2        # m
    x_ball_init = 0
    y_ball_init = 0
    z_ball_init = 0
    speed = 10       # m/s

    hang=13 # min hang
    vang=0   # min vang

    hang=38 # max hang
    vang=19  # max vang

    print(final_position(x_ball_init,y_ball_init,z_ball_init,speed,hang,vang,x_final,target_size))

if __name__ == "__main__":
    main()
