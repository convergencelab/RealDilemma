from settings import POLICYF, HOSTNAME

import json
with open(POLICYF, "r") as f:
    POLICIES = json.load(f)

def run_policy(num_steps, policy_dict=POLICIES) -> str:
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
          
    return json.dump(results)