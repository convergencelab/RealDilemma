import tensorflow
print(tensorflow.__version__)
import gym
import json
import datetime as dt
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.env_checker import check_env
from stable_baselines import PPO2
from gym_pibot.envs.pibot_env2 import PiBotEnv2
env = PiBotEnv2()

# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)
# we must reset env because of RPI GPIO
del env
# The algorithms require a vectorized environment to run
# env = DummyVecEnv([PiBotEnv])
#
#
#
# model = PPO2(MlpPolicy, env, verbose=1)
#
# model.learn(total_timesteps=200)
# obs = env.reset()
#
# for i in range(3):
#   action, _states = model.predict(obs)
#   print("*********ACTION************")
#   print(action, _states)
#   print("**********ACTION************")
#  # obs, rewards, done, info = env.step(action)
#  # env.render()
#  # if done:
#   #  print("Goal reached!", "reward=", reward)
#    # break