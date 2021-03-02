import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PiBot2 import PiBot2
import numpy as np

ENERGY_THRES = 4000# thres for total amount of different motors used in robo
MAX_REWARD = 1000


class PiBotEnv2(gym.Env):
  """
  standard env for PiBot
  this is the most basic implementation of the robotic system.
  """
  metadata = {'render.modes': ['human']}

  def __init__(self):
      super(PiBotEnv2, self).__init__()
      self.PiBot = PiBot2() # we are using the newer pibot
      self.CONTROL_LOOKUP = {
          0: self.PiBot.forward,
          1: self.PiBot.backward,
          2: self.PiBot.turn_cw,
          3: self.PiBot.turn_ccw,
          4: self.PiBot.stop
         # 4: self.PiBot.turn_servo
      }

      self.reward_range = (0, MAX_REWARD)
      self.action_space = spaces.Dict({
          "Action": spaces.Discrete(4),
          "PWM": spaces.Box(low=np.array([0]), high=np.array([100])),
          "Time": spaces.Box(low=np.array([0]), high=np.array([5]))
      }
      )
      # Initial observation will just be the ultrasound sensor and amount of distance travelled (either forward or backward)
      #self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([4, 1000]), dtype=np.int32)
      self.observation_space = spaces.Dict({
            "action":spaces.Discrete(4),
            "us_readings":spaces.Box(low=np.zeros(self.PiBot._us_res), high=np.full(self.PiBot._us_res, 5000)),
            "score":spaces.Box(low=np.zeros(self.PiBot._us_res), high=np.full(self.PiBot._us_res, 1)),
            "total_score":spaces.Box(low=np.array([0]), high=np.array([MAX_REWARD]))
        })
  def reset(self):
    """
    no reset for this one
    :return:
    """
    # initial condition

    self.PiBot.reset()
    state = self.PiBot.get_state()

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
      print(ob)
      # sum of actions >= energy thres
      done = bool(sum(self.PiBot.get_total_actions()) >= ENERGY_THRES)

      return ob, reward, done, {}

  def do_action(self, action):
      """ Converts the action space into PiBot action"""
      do = self.CONTROL_LOOKUP[action["Action"]]
      duty  = action["PWM"]
      time = action["Time"]
      # perform action
      do(duty, time)

  def _get_reward(self):
      """
      we want to reward total score, but also reward an increasing series of score
      :return:
      """
      # maximize amount of movement, maximize distance in ultrasound sensor
      _, us_readings, score, total_score = self._get_state()
      del_x  = self._score_grad_1d(us_readings)
      reward = total_Score + del_x# an increase in distance + remaining in distance thres
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
      # pass






