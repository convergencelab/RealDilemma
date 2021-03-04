import socket
"""
connecting main node to pis
"""
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)  # Server ip
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

def send(addr, data):
    s.sendto(data.encode('utf-8'), addr)

