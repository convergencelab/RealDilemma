import tensorflow
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
    #"ACER": partial(ACER, policy=MlpPolicy, verbose=1),
    # "ACKTR": partial(ACKTR, policy=MlpPolicy, verbose=1),
    # "DQN": partial(DQN, policy=MlpPolicy, verbose=1),
    "PPO2": partial(PPO2, policy=MlpPolicy, verbose=1),
    "A2C": partial(A2C, policy=MlpPolicy, verbose=1),


}

def train_session(pibot, steps, train_dict=TRAIN_DICT, continue_prompt=False):
    """
    wrap train dict with training function
    """
    for model, func in train_dict.items():
        print(f"TRAINING: {model}")
        train(steps, pibot, func, model)
        if continue_prompt:
            input("hit enter to continue: ")

def train(steps, pibot, model, model_name) -> str:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    # record actions
    env._RECORD_ACTION = True
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    d_env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    model = model(env=d_env)
    model.learn(total_timesteps=steps)
    fpath = os.path.join(TRAIN_DIR, model_name)
    model.save(fpath)
    with open(POLICYF, "r") as f:
      policies = json.load(f)
      policies[model_name] = fpath
    with open(POLICYF, "w") as f:
        json.dump(policies, f)
    env._record_actions(model_name+"_TRAINING")

    return fpath
