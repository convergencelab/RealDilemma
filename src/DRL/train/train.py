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
from src.Pi.PiBot.PiBot2 import PiBot2
from functools import partial

from settings import TRAINF, POLICYF


def train_PPO2(steps) -> str:
    # If the environment don't follow the interface, an error will be thrown
    pibot = PiBot2()
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, Name)
    model.save(fpath)
    with open(POLICYF, "R") as f:
      policies = json.load(f)
    policies["PPO2"] = fpath
    json.dump(policies, POLICYF)
    del pibot
    del env
    return fpath