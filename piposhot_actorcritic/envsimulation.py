#!/usr/bin/env python

#MIT License
#Copyright (c) 2017 Massimiliano Patacchiola
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.


#Class for creating a gridworld of arbitrary size and with arbitrary obstacles.
#Each state of the gridworld should have a reward. The transition matrix is defined
#as the probability of executing an action given a command to the robot.

import numpy as np
from ballmodel import *

class GridWorld:

    def __init__(self, tot_row, tot_col):
        #The world is a matrix of size row x col
        self.world_row = tot_row
        self.world_col = tot_col
        self.reward_matrix = np.zeros((tot_row, tot_col))
        self.state_matrix = np.zeros((tot_row, tot_col))
        #The transition matrix stores the probabilities of performing a certain action
        #when a command is given
        self.action_space_size = 4
        self.transition_matrix = np.eye(self.action_space_size)
        #Begin at a random position
        self.position = [np.random.randint(tot_row), np.random.randint(tot_col)]

    def setTransitionMatrix(self, transition_matrix):
        '''Set the transition matrix.
        The transition matrix here is intended as a matrix which has a line
        for each action and the element of the row are the probabilities to
        executes each action when a command is given.
        '''
        if(transition_matrix.shape != self.transition_matrix.shape):
            raise ValueError('The shape of the two matrices must be the same.')
        self.transition_matrix = transition_matrix

    def setRewardMatrix(self, reward_matrix):
        '''Set the reward matrix.
        '''
        if(reward_matrix.shape != self.reward_matrix.shape):
            raise ValueError('The shape of the matrix does not match with the shape of the world.')
        self.reward_matrix = reward_matrix

    def setStateMatrix(self, state_matrix):
        '''Set the obstacles in the world.
        The input to the function is a matrix with the
        same size of the world
        -1 for states which are not walkable.
        +1 for terminal states
         0 for all the walkable states (non terminal)
        '''
        if(state_matrix.shape != self.state_matrix.shape):
            raise ValueError('The shape of the matrix does not match with the shape of the world.')
        self.state_matrix = state_matrix

    def setPosition(self, index_row=None, index_col=None):
        ''' Set the position of the robot in a specific state.
        If no indeces are given, the new position is random.
        '''
        if(index_row is None or index_col is None): self.position = [np.random.randint(tot_row), np.random.randint(tot_col)]
        else: self.position = [index_row, index_col]

    def reset(self, exploring_starts=False):
        ''' If exploring_starts is set to True, set the robot's position to a random one.
        Else, set the position of the robot in the bottom left corner.
        It returns the first observation
        '''
        if exploring_starts:
            while(True):
                hang_init = np.random.randint(13,38+1)
                vang_init = np.random.randint(0,19+1)
                row, col = final_position(x_ball_init=0, y_ball_init=0, z_ball_init=0, speed=10,
                            hang=hang_init, vang=vang_init,x_final=2,target_size=0.1)
                if(self.state_matrix[row, col] == 0): break
            self.position = [row, col]
        else:
            self.position = [0, 0]
            hang_init = 13
            vang_init = 0
        return self.position, hang_init, vang_init

    def step(self, action, hang_init, vang_init):
        ''' One step in the world.
        [observation, reward, done = env.step(action)]
        The robot moves one step in the world based on the action given.
        The action can be 0=vang+1, 1=hang+1, 2=vang-1, 3=hang-1
        @return observation the position of the robot after the step
        @return reward the reward associated with the next state
        @return done True if the state is terminal
        '''
        if(action >= self.action_space_size):
            raise ValueError('The action is not included in the action space.')

        #Choose randomly a new action to perform
        action = np.random.choice(4, 1, p=self.transition_matrix[int(action),:])

        #Generate the new position based on the current position and action
        if(action == 0):
            vang_init+=1
            new_position = final_position(hang=hang_init, vang=vang_init)  #vang+1
        elif(action == 1):
            hang_init+=1
            new_position = final_position(hang=hang_init, vang=vang_init)  #hang+1
        elif(action == 2):
            vang_init-=1
            new_position = final_position(hang=hang_init, vang=vang_init)  #vang-1
        elif(action == 3):
            hang_init-=1
            new_position = final_position(hang=hang_init, vang=vang_init)  #hang-1
        else: raise ValueError('The action is not included in the action space.')

        #Update the position if the new one is valid
        if (new_position[0]>=0 and new_position[0]<self.world_row):
            if(new_position[1]>=0 and new_position[1]<self.world_col):
                if(self.state_matrix[new_position[0], new_position[1]] != -1):
                    self.position = new_position

        reward = self.reward_matrix[self.position[0], self.position[1]]
        #Done is True if the state is a terminal state
        done = bool(self.state_matrix[self.position[0], self.position[1]])
        return self.position, reward, hang_init, vang_init, done
