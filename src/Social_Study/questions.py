import json
from settings import RESPONSE_FILE, QUESTIONS_FILE


def get_user_input():
    with open(QUESTIONS_FILE, "r") as f:
        data = json.load(f)
    for q in data.keys():
        data[q] = input(q)
    log_data(data)
    return data

def log_data(user_input):
    """
    we will save the policy displayed as json

    we will need to make it such that the pi can send this data back to the main node
    :param user_input:
    :param policy_displayed:
    :return:
    """
    with open(RESPONSE_FILE, "w") as f:
        json.dump(user_input, f)

