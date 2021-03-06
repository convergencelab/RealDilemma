from src.DRL.train.train import train_PPO2
from src.DRL.test.test import run_policy
from src.Pi.PiBot.PiBot2 import PiBot2
import json

def train_and_test_bot():
    """
    testing training and testing with bots
    :return:
    """
    pibot = PiBot2()
    train_PPO2(2500, pibot)
    print("running policy")
    outcome = run_policy(200, pibot)
   # outcome = {"testing":100}
   # outcome = json.dumps(outcome)
    print(outcome.replace(" ", ""))
    return outcome.replace(" ", "")



