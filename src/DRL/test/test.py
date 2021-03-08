from settings import POLICYF, HOSTNAME
from stable_baselines import PPO2, A2C
from stable_baselines.common.policies import MlpPolicy, ActorCriticPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.env_checker import check_env
from gym_pibot.envs.pibot_env2 import PiBotEnv2
from functools import partial
import json
with open(POLICYF, "r") as f:
    POLICIES = json.load(f)

def run_policy(pibot,num_steps, policy_dict=POLICIES, continue_prompt=False) -> None:
    # If the environment don't follow the interface, an error will be thrown
    env = PiBotEnv2(pibot)
    # record actions
    env._RECORD_ACTION = True
    check_env(env, warn=True)
    d_env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    for k, v in policy_dict.items():
        if "PPO2" in k:
            model = PPO2.load(v)
        if "A2C" in k:
            model = A2C.load(v)
        obs = d_env.reset()
        for i in range(num_steps):
          action, _states = model.predict(obs)
          obs, rewards, done, info = env.step(action)
        env._record_actions(k+"_INFERENCE")
        if continue_prompt:
            input("hit enter to continue: ")
