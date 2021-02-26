import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PiBot import PiBot
import numpy as np

ENERGY_THRES = 4000# thres for total amount of different motors used in robo
MAX_REWARD = 1000


class PiBotEnv(gym.Env):
  """
  standard env for PiBot
  this is the most basic implementation of the robotic system.
  """
  metadata = {'render.modes': ['human']}

  def __init__(self):
      super(PiBotEnv, self).__init__()
      self.PiBot = PiBot()
      self.CONTROL_LOOKUP = {
          0: self.PiBot.forward,
          1: self.PiBot.backward,
          2: self.PiBot.turn_cw,
          3: self.PiBot.turn_ccw,
          4: self.PiBot.turn_servo
      }

      self.reward_range = (0, MAX_REWARD)
      # Actions: [[0:Forwards, 1:Backwards, 2:turn_cw, 3:turn_ccw, 4:Turn Servo], power]
      #.action_space = spaces.Box(
      #    low=np.array([0, 0]), high=np.array([5, 10]))
      #self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([4, 10]), dtype=np.int32)
      self.action_space = spaces.Discrete(5)
      # Initial observation will just be the ultrasound sensor and amount of distance travelled (either forward or backward)
      self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([4, 1000]), dtype=np.int32)

  def reset(self):
    """
    no reset for this one
    :return:
    """
    # initial condition

    self.PiBot.reset()
    return self.PiBot.get_state()

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
      print(ob)
      # sum of actions >= energy thres
      done = bool(sum(self.PiBot.get_total_actions()) >= ENERGY_THRES)

      return ob, reward, done, {}

  def do_action(self, action):
      """ Converts the action space into PiBot action"""
      control = self.CONTROL_LOOKUP[action[0]]
      # perform action with a default of 1s
      #control(action[1])
      control(1)

  def _get_reward(self):
      """
      reward is abs difference between ultrasound sensor and amount of distance travelled
      :return:
      """
      # maximize amount of movement, maximize distance in ultrasound sensor
      state = self._get_state()
      return float(state[0] + state[1])

  def _get_state(self):
      """
      state will just be reading ultrasound at first, we should make
      this better...
      :return:
      """
      return self.PiBot.get_state()

  def close(self):
      del self.PiBot
      pass






