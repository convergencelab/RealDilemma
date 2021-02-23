import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PiBot import PiBot
import numpy as np

ENERGY_THRES = 4000# thres for total amount of different motors used in robo
MAX_REWARD = 1000


class PiBotEnv(gym.Env):
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
      self.action_space = spaces.Box(
          low=np.array([0, 0]), high=np.array([5, 10]), dtype=np.float16)
      # Initial observation will just be the ultrasound sensor and amount of distance travelled (either forward or backward)
      self.observation_space = spaces.Box(
          low=np.array([0]), high=np.array([1000]), dtype=np.float16)
      # initial condition
      self.state = None

  def _step(self, action):
      """
      no ending of episode yet, must determine what this means exactly
      same with info
      :param action:
      :return:
      """
      self._take_action(action)
      # self.status = self.env.step()
      reward = self._get_reward()
      ob = self._getState()
      if np.sum(self.PiBot.get_total_actions) >= ENERGY_THRES:
          done = True
      else:
          done = False

      return ob, reward, done, {}

  def _take_action(self, action):
      """ Converts the action space into PiBot action"""
      action = self.CONTROL_LOOKUP[action[0]]
      # perform action with the desginated duty
      action(action[1])

  def _get_reward(self):
      """
      reward is abs difference between ultrasound sensor and amount of distance travelled
      :return:
      """
      # maximize amount of movement, maximize distance in ultrasound sensor
      state = self._get_state()
      return state[0] + state[1]

  def _get_state(self):
      """
      state will just be reading ultrasound at first, we should make
      this better...
      :return:
      """
      return self.PiBot.get_state()


  def reset(self):
    """
    no reset for this one
    :return:
    """
    self.PiBot.reset()



