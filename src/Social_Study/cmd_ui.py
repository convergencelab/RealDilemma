import json

with open("./Questions.json", "r") as f:
    data = json.load(f)

def get_user_input():
    with open("./Questions.json", "r") as f:
        data = json.load(f)
    for q in data.keys():
        data[q] = input(q)
    return data
def log_data(user_input, policy_displayed):
    """
    we will save the policy displayed as json

    we will need to make it such that the pi can send this data back to the main node
    :param user_input:
    :param policy_displayed:
    :return:
    """

print(data)