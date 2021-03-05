import socket
import json
from settings import RPIS, MAIN_NODE_HOST_NAME, H_TITLE, OUTPUT_FILE
import os
"""
connecting main node to pis
"""


def publish_data(data):
    """
    we are susing broker service: publish data
    :param data:
    :return:
    """
    os.system(f" mosquitto_pub -h {MAIN_NODE_HOST_NAME} -t {H_TITLE} -m {data}")

def subscribe():
    os.system(f" mosquitto_sub -h {MAIN_NODE_HOST_NAME} -t {H_TITLE} > {OUTPUT_FILE}")

def read_output_file():
    with open(OUTPUT_FILE, "r") as f:
        data = f.readlines()
    return data


