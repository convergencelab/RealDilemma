from src.DRL.train.train import train_PPO2
from src.DRL.test.test import run_policy


def train_and_test_bot():
    """
    testing training and testing with bots
    :return:
    """
    train_PPO2(200)
    outcome = run_policy(200)
    return outcome



