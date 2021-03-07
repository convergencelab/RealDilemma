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

TRAIN_DICT = {
    "PPO2": partial(PPO2, policy=MlpPolicy, verbose=1),
    "A2C": partial(A2C, policy=MlpPolicy, verbose=1),

}

def train_session(pibot, steps, train_dict=TRAIN_DICT):
    """
    wrap train dict with training function
    """
    for model, func in train_dict.items():
        train(steps, pibot, func, model)

def train(steps, pibot, model, model_name) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = model(env=env)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, model_name)
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
      policies[model_name] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    del pibot
    del env
    return fpath

def train_PPO2_w_servo(steps, pibot) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot, servo=True)])
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, HOSTNAME+"_PPO2_W_SERVO")
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
    policies["PPO2_W_SERVO"] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    del pibot
    del env
    return fpath

def train_A2C(steps, pibot) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = A2C(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, HOSTNAME+"_A2C")
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
    policies["A2C"] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    del pibot
    del env
    return fpath

def train_A2C_SERVO(steps, pibot) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot, servo=False)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = A2C(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, HOSTNAME+"_A2C")
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
    policies["A2C"] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    del pibot
    del env
    return fpath