from src.DRL.train.train import train_PPO2, train_PPO2_w_servo, train_A2C
from src.DRL.test.test import run_policy
from src.Pi.PiBot.PiBot2 import PiBot2
import json

def train_and_test_bot():
    """
    testing training and testing with bots
    :return:
    """
    pibot = PiBot2()
    # train_PPO2(2500, pibot)
    # train_PPO2_w_servo(5, pibot)
    train_A2C(5, pibot)
    print("running policy")
    outcome = run_policy(5, pibot)
   # outcome = {"testing":100}
   # outcome = json.dumps(outcome)
    print(outcome.replace(" ", ""))
    return outcome.replace(" ", "")



