import gym
from gym import error, spaces, utils
from gym.utils import seeding
from src.Pi.PiBot.PiBot2 import PiBot2
import numpy as np

ENERGY_THRES = 4000# thres for total amount of different motors used in robo
MAX_REWARD = 1000


class PiBotEnv2(gym.Env):
  """
  standard env for PiBot
  this is the most basic implementation of the robotic system.
  """
  metadata = {'render.modes': ['human']}

  def __init__(self, PiBot, servo=False):
      super(PiBotEnv2, self).__init__()
      self.PiBot = PiBot # we are using the newer pibot
      self.SERVO = servo
      self.CONTROL_LOOKUP = {
          0: self.PiBot.forward,
          1: self.PiBot.backward,
          2: self.PiBot.turn_cw,
          3: self.PiBot.turn_ccw,
          4: self.PiBot.stop,
          5: self.PiBot._servo
      }
      if self.SERVO:
          #self.reward_range = (0, MAX_REWARD)
          self.action_space = spaces.MultiDiscrete([6,# action
                                                    5,# PWM
                                                    5]# time
                                                    )
      else:
          self.reward_range = (0, MAX_REWARD)
          self.action_space = spaces.MultiDiscrete([5,  # action
                                                    5,  # PWM
                                                    5]  # time
                                                   )
      # action, diff(us_readings), total_score
      self.observation_space = spaces.Box(low=np.full(3, -5000), high=np.full(3, 5000), dtype=np.float32)

  def reset(self):
    """
    no reset for this one
    :return:
    """
    # initial condition

    self.PiBot.reset()
    state = self._get_state()

    return state

  def step(self, action):
      """
      no ending of episode yet, must determine what this means exactly
      same with info
      :param action:
      :return:
      """
      self.do_action(action)
      reward = self._get_reward()
      ob = self._get_state()
      # sum of actions >= energy thres
      done = bool(self.PiBot.get_total_actions() >= ENERGY_THRES)

      return ob, reward, done, {}

  def do_action(self, action):
      """ Converts the action space into PiBot action"""
      do = self.CONTROL_LOOKUP[action[0]]
      duty  = 100 - action[1]
      time = action[2]
      # perform action
      do(duty, time)

  def _get_reward(self):
      """
      we want to reward total score, but also reward an increasing series of score
      :return:
      """
      # maximize amount of movement, maximize distance in ultrasound sensor
      state = self._get_state()
      # diff(X) + score
      reward = state[1] + state[2]
      return reward

  def _score_grad_1d(self, us_Readings):
      """
      reward a sequence that measures an steady increase in distance
      :param us_Readings:
      :return:
      """
      dx = np.diff(us_Readings) # compute 1d difference
      return dx


  def _get_state(self):
      """
      state will just be reading ultrasound at first, we should make
      this better...
      :return:
      """
      return self.PiBot.get_state()

  def close(self):
      del self.PiBot






