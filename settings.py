import socket
import os
"""
To set some things straight
"""
POLICYF = "/home/pi/RealDilemma/src/DRL/test/policies.json"
TRAIN_DIR = "/home/pi/saved_models"

MAIN_NODE_HOST_NAME = 'Jimi'
PC = 'DESKTOP-5F7T77V'
H_TITLE = "PI_DRL"

HOSTNAME = socket.gethostname()
if HOSTNAME == PC:
    # ensure that mosquitto is in the path
    ACTION_FILE = r".\actions.txt"
    RESPONSE_FILE = r".\responses.json"
else:
    ACTION_FILE = "/home/pi/RealDilemma/actions.txt"
    RESPONSE_FILE = r"/home/pi/RealDilemma/responses.json"

QUESTIONS_FILE = "./Questions.json"
RPIS = {
          "Jimi": "192.168.137.63",
          "Frank": "192.168.137.118",
          "Siracha":"192.168.137.152"
        }

PI_HOST_NAMES = RPIS.keys()

VIDEO_STREAM = "http://141.109.108.67:8080/video"