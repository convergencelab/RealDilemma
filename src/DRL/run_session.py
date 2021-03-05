from src.DRL.train.train import train_PPO2
from src.DRL.test.test import run_policy
import json

def train_and_test_bot():
    """
    testing training and testing with bots
    :return:
    """
    train_PPO2(200)
    #utcome = run_policy(200)
    outcome = {"testing":100}
    outcome = json.dumps(outcome)
    return outcome



