import socket
import os
"""
To set some things straight
"""
POLICYF = "/home/pi/RealDilemma/src/DRL/test/policies.json"
TRAINF = "/home/pi/RealDilemma/src/DRL/train/saved_models"

MAIN_NODE_HOST_NAME = 'Jimi'
PC = 'DESKTOP-5F7T77V'
H_TITLE = "PI_DRL"

HOSTNAME = socket.gethostname()
if HOSTNAME == PC:
    # ensure that mosquitto is in the path
    OUTPUT_FILE = r".\actions.txt"
else:
    OUTPUT_FILE = "/home/pi/RealDilemma/actions.txt"

RPIS = {
          "Jimi": "192.168.137.63"
        }

PI_HOST_NAMES = RPIS.keys()