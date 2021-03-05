from src.main_node.Communication.main_node import *
import settings
"""
determine if main or pi
"""
import socket
hostname = socket.gethostname()
if hostname in settings.PI_HOST_NAMES:
    IS_PI = True
    from src.DRL.run_session import train_and_test_bot
elif hostname == settings.MAIN_NODE_HOST_NAME:
    IS_PI = False
    from src.main_node.Utils.OverHead import OverHead
    # from src.main_node.Utils.stream_oh_inference import run
else:
    raise Exception("Must configure this device in settings.py")

def main_train_and_test():
    if not IS_PI:
        # oh_stream = OverHead()
        # model = ('ssd_mobilenet_v2_320x320_coco17_tpu-8', 3)
        # run(model, oh_stream)
        sendall("1") # initiate all bots
        print("msg sent")
        #msg = wait_for_msg()
        #print(msg)
    else:
        print("waiting for msg")
        msg = wait_for_msg()
        if msg == "1":
            #outcome = train_and_test_bot()
            outcome = "testing this out"
            addr = socket.gethostbyname(hostname)
            send(outcome, settings.MAIN_NODE_HOST_NAME)




if __name__ == "__main__":

    # main()
    main_train_and_test()

    
