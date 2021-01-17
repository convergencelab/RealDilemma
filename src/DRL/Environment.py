from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

tf.compat.v1.enable_v2_behavior()

"""
Tensorflow environment for problem:


Environment for Robots:
    1. At every time step agent is given its position
    2. Can take up to three actions, can stop at any point
    
    Actions: Robot can move forwards, backwards, or rotate: function on time metrics not actual distance metrics
    Observations: Current position on map, position of destination 
    Reward: Objective is for robot to get to location in map reward = euclidean distance from destination on map
"""

class SimplifiedRoboEnv(py_environment.PyEnvironment):
    def __init__(self, map_size=(500, 500), init_state=None):
        self.map_size = map_size
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(2,), dtype=np.float32, minimum=-10, maximum=10, name='action') # forwards (+), backwards(-), rotate left(+), rotate right(-)
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1, 2, 3), dtype=np.float32, minimum=0, maximum=map_size[0], name='observation') # two locations: desired position and current position

        # if no state is provided randomly place robots somewheres
        if not init_state:
            self._state = self.gen_random_state()
        else:
            self._state = init_state
        self._episode_ended = False

        # self.max_step = 200
        self.total_steps = 0
        self.dist_threshold = 10.0



    def gen_random_state(self):
        # x, y, direction
        pos = np.random.randint(low=0, high=self.map_size[0]), np.random.randint(low=0, high=self.map_size[1]), np.random.randint(low=0, high=360)
        dest = np.random.randint(low=0, high=self.map_size[0]), np.random.randint(low=0, high=self.map_size[1]), 0
        return np.array([pos, dest], dtype=np.float32)

    def update_state(self, action):
        travel, yaw = action
        # direction
        cur_angle = self._state[0][2]
        # add new angle
        cur_angle+=(yaw*360)
        if cur_angle < 0:
            cur_angle= 360 + cur_angle # compliment
        cur_angle%=360 # maintain 360deg
        self._state[0][2] = cur_angle
        # calculate new pos, must remain within boundaries of map
        x = self._state[0][0]
        y = self._state[0][1]
        self._state[0][0] = max(min((travel*np.cos(cur_angle))+x, self.map_size[0]), 0)
        self._state[0][1] = max(min((travel*np.sin(cur_angle))+y, self.map_size[1]), 0)

    def get_state(self):
        return self._state
    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        # self._state = self.get_new_state() keep the state the same.
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.float32))

    def _step(self, action):
       #  self.total_steps+=1
        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()
        # forwards (+), backwards(-), rotate left(+), rotate right(-)
        # enforce boundaries of map
        self.update_state(action)
        # euclidean distance
        euc_dist = np.average(abs(self._state[1][0:2] - self._state[0][0:2]))  # distance
        #if self.total_steps == self.max_step or euc_dist < self.dist_threshold:

        if euc_dist < self.dist_threshold:
            self._episode_ended = True

        if self._episode_ended:
            # maximize negative val, euc distance from targ + regularized num steps
            reward = - euc_dist
            return ts.termination(np.array([self._state], dtype=np.float32), reward)

        else:
            return ts.transition(
                np.array([self._state], dtype=np.float32), reward=-euc_dist, discount=1.0)




class EvenSimplerRoboEnv(py_environment.PyEnvironment):
    def __init__(self, map_size=(500, 500), init_state=None):
        self.map_size = map_size
        # 4 actions move forwards 0
        # backwards 1
        # turn left, 2
        # turn right 3
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.float32, minimum=0, maximum=3, name='action') # forwards (+), backwards(-), rotate left(+), rotate right(-)
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1, 2, 3), dtype=np.float32, minimum=0, maximum=map_size[0], name='observation') # two locations: desired position and current position

        # if no state is provided randomly place robots somewheres
        if not init_state:
            self._state = self.gen_random_state()
        else:
            self._state = init_state
        self._episode_ended = False

        self.max_step = 100000
        self.total_steps = 0
        self.dist_threshold = 10.0
        self.step_size = 10

    def gen_random_state(self):
        # x, y, direction
        pos = np.random.randint(low=0, high=self.map_size[0]), np.random.randint(low=0, high=self.map_size[1]), 0
        dest = np.random.randint(low=0, high=self.map_size[0]), np.random.randint(low=0, high=self.map_size[1]), 0
        return np.array([pos, dest], dtype=np.float32)

    def update_state(self, action):
        x = self._state[0][0]
        y = self._state[0][1]
        dir = self._state[0][2]
        if action == 0: # forward
            if dir == 0: # 0 deg
                self._state[0][0] = max(min(self.step_size+x, self.map_size[0]), 0) # update x
            if dir == 1: # 90 deg
                self._state[0][1] = max(min(self.step_size+y, self.map_size[1]), 0)  # update y
            if dir == 2: # 180 deg
                self._state[0][0] = max(min(x-self.step_size, self.map_size[0]), 0)  # update x
            if dir == 3: # 270 deg
                self._state[0][0] = max(min(y-self.step_size, self.map_size[0]), 0)  # update y

        if action == 1: # backward
            if dir == 0: # 0 deg
                self._state[0][0] = max(min(x-self.step_size, self.map_size[0]), 0) # update x
            if dir == 1: # 90 deg
                self._state[0][1] = max(min(y-self.step_size, self.map_size[1]), 0)  # update y
            if dir == 2: # 180 deg
                self._state[0][0] = max(min(self.step_size+x, self.map_size[0]), 0)  # update x
            if dir == 3: # 270 deg
                self._state[0][0] = max(min(self.step_size+y, self.map_size[0]), 0)  # update y

        if action == 2:  # turn left
            self._state[0][2] = abs((dir-1)%3)

        if action == 3:  # turn right
            self._state[0][2] = abs((dir+1)%3)

    def get_state(self):
        return self._state
    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        # self._state = self.get_new_state() keep the state the same.
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.float32))

    def _step(self, action):
        self.total_steps+=1
        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()
        # forwards (+), backwards(-), rotate left(+), rotate right(-)
        # enforce boundaries of map
        self.update_state(action)
        # euclidean distance
        euc_dist = np.average(abs(self._state[1][0:2] - self._state[0][0:2]))  # distance
        #if self.total_steps == self.max_step or euc_dist < self.dist_threshold:

        if euc_dist < self.dist_threshold:
            self._episode_ended = True

        if self._episode_ended or self.total_steps > self.max_step:
            # maximize negative val, euc distance from targ + regularized num steps
            reward = - euc_dist
            return ts.termination(np.array([self._state], dtype=np.float32), reward)

        else:
            return ts.transition(
                np.array([self._state], dtype=np.float32), reward=-euc_dist, discount=1.0)



