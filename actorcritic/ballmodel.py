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
    tilt=45, pan=0, x_final=2,target_size=0.1):
    g = 9.81       # m.s^-2
    x_speed = speed*np.cos(tilt*np.pi/180)*np.cos(pan*np.pi/180)
    y_speed = speed*np.sin(pan*np.pi/180)
    z_speed = speed*np.sin(tilt*np.pi/180)

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

    tilt=13 # min tilt
    pan=0   # min pan

    tilt=38 # max tilt
    pan=19  # max pan

    print(final_position(x_ball_init,y_ball_init,z_ball_init,speed,tilt,pan,x_final,target_size))

if __name__ == "__main__":
    main()
