from settings import POLICYF, HOSTNAME
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy, ActorCriticPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.env_checker import check_env
from gym_pibot.envs.pibot_env2 import PiBotEnv2
from functools import partial
import json
with open(POLICYF, "r") as f:
    POLICIES = json.load(f)

def run_policy(num_steps,pibot, policy_dict=POLICIES) -> str:
    env = PiBotEnv2(pibot)
    check_env(env, warn=True)
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([partial(PiBotEnv2, PiBot=pibot)])
    results = {"DEVICE_NAME":HOSTNAME,
               "POLICIES":[]}
    for k, v in policy_dict.items():
        results["POLICIES"].append(k)
        if k == "PPO2":
            model = PPO2.load(v)
        obs = env.reset()
        results[k] = []
        for i in range(num_steps):
          action, _states = model.predict(obs)
          results[k].append(action)
          obs, rewards, done, info = env.step(action)
        print(results)
    return json.dumps(results)
