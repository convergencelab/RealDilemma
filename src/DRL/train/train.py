import tensorflow
print(tensorflow.__version__)
import gym
import json
import datetime as dt
from stable_baselines.common.policies import MlpPolicy, ActorCriticPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.env_checker import check_env
from stable_baselines import PPO2, A2C
from gym_pibot.envs.pibot_env2 import PiBotEnv2
from functools import partial
import os
from settings import TRAIN_DIR, POLICYF, HOSTNAME


def train_PPO2(steps, pibot) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, HOSTNAME)
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
    policies["PPO2"] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    del pibot
    del env
    return fpath