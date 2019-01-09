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
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import numpy as np
from envsimulation import GridWorld
import matplotlib.pyplot as plt

def softmax(x):
    '''Compute softmax values of array x.
    @param x the input array
    @return the softmax array
    '''
    return np.exp(x - np.max(x)) / np.sum(np.exp(x - np.max(x)))

def update_critic(utility_matrix, observation, new_observation,
                   reward, alpha, gamma, done):
    '''Return the updated utility matrix
    @param utility_matrix the matrix before the update
    @param observation the state obsrved at t
    @param new_observation the state observed at t+1
    @param reward the reward observed after the action
    @param alpha the step size (learning rate)
    @param gamma the discount factor
    @return the updated utility matrix
    @return the estimation error delta
    '''
    u = utility_matrix[observation[0], observation[1]]
    u_t1 = utility_matrix[new_observation[0], new_observation[1]]
    delta = reward + ((gamma * u_t1) - u)
    utility_matrix[observation[0], observation[1]] += alpha * delta
    return utility_matrix, delta

def update_actor(state_action_matrix, observation, action, delta, beta_matrix=None):
    '''Return the updated state-action matrix
    @param state_action_matrix the matrix before the update
    @param observation the state obsrved at t
    @param action taken at time t
    @param delta the estimation error returned by the critic
    @param beta_matrix a visit counter for each state-action pair
    @return the updated matrix
    '''
    col = observation[1] + (observation[0]*4)
    if beta_matrix is None: beta = 1
    else: beta = 1 / beta_matrix[action,col]
    state_action_matrix[action, col] += beta * delta
    return state_action_matrix

def main():

    size_grid_x = 10
    size_grid_y = 10
    nb_action = 4
    x_target = 4
    y_target = 4

    env = GridWorld(size_grid_x, size_grid_y)

    #Define the state matrix
    state_matrix = np.zeros((size_grid_x,size_grid_y))
    state_matrix[x_target, y_target] = 1
    print("State Matrix:")
    print(state_matrix)

    #Define the reward matrix
    reward_matrix = np.full((size_grid_x,size_grid_y), -0.04)
    reward_matrix[x_target, y_target] = 10
    print("Reward Matrix:")
    print(reward_matrix)

    #Define the transition matrix
    transition_matrix = np.eye(nb_action)

    state_action_matrix = np.random.random((nb_action,size_grid_x*size_grid_y))
    print("State-Action Matrix:")
    print(state_action_matrix)

    env.setStateMatrix(state_matrix)
    env.setRewardMatrix(reward_matrix)
    env.setTransitionMatrix(transition_matrix)

    utility_matrix = np.zeros((size_grid_x,size_grid_y))
    print("Utility Matrix:")
    print(utility_matrix)

    gamma = 0.999
    alpha = 0.001 #constant step size
    # beta_matrix = np.zeros((nb_action,size_grid_x*size_grid_y))
    tot_epoch = 3000
    print_epoch = 100


    plt.ion()
    fig = plt.figure(0)
    ax = fig.add_subplot(1,1,1)
    ax.imshow(utility_matrix)

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(1,1,1)
    ax1.imshow(state_action_matrix)

    for epoch in range(tot_epoch):
        #Reset and return the first observation
        observation, tilt, pan = env.reset(exploring_starts=True)
        for step in range(50):
            #Estimating the action through Softmax
            col = observation[1] + (observation[0]*4)
            action_array = state_action_matrix[:, col]
            action_distribution = softmax(action_array)
            action = np.random.choice(nb_action, 1, p=action_distribution)

            #To enable the beta parameter, enable the libe below
            #and add beta_matrix=beta_matrix in the update actor function
            #beta_matrix[action,col] += 1 #increment the counter

            #Move one step in the environment and get obs and reward
            new_observation, reward, tilt, pan, done = env.step(action, tilt, pan)
            utility_matrix, delta = update_critic(utility_matrix, observation,
                                                  new_observation, reward, alpha, gamma, done)
            state_action_matrix = update_actor(state_action_matrix, observation,
                                               action, delta, beta_matrix=None)
            observation = new_observation
            if done: break


        if(epoch % print_epoch == 0):
            # print("")
            # print("Utility matrix after " + str(epoch+1) + " iterations:")
            # print(utility_matrix)
            # print("")
            # print("State-Action matrix after " + str(epoch+1) + " iterations:")
            # print(state_action_matrix)
            # env.render()

            print(epoch)
            plt.clf()
            ax = fig.add_subplot(1,1,1)
            ax.imshow(utility_matrix)

            ax1 = fig1.add_subplot(1,1,1)
            ax1.imshow(state_action_matrix)

            fig.canvas.draw()
            fig1.canvas.draw()

    #Time to check the utility matrix obtained
    print("Utility matrix after " + str(tot_epoch) + " iterations:")
    print(utility_matrix)
    print("State-Action matrix after  " + str(tot_epoch) + " iterations:")
    print(state_action_matrix)



if __name__ == "__main__":
    main()
