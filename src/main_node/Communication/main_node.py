import socket
import json
from settings import RPIS, MAIN_NODE_HOST_NAME
"""
connecting main node to pis
"""
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)  # Server ip
PORT = 4000
S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
S.bind((HOST, PORT))

def sendall(data):
    if HOSTNAME != MAIN_NODE_HOST_NAME:
        raise Exception("sendall only for host node")
    for _, addr in RPIS:
        send(data, addr)

def send(data, addr):
    s.sendto(data.encode('utf-8'), addr)

def wait_for_msg():
    while True:
        data = S.recv(1024)
        print(data)
