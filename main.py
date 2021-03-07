from src.main_node.Communication.Communication import *
import settings
import socket
import threading
from src.Social_Study import questions
from src.Pi.PiBot.PiBot2 import PiBot2
"""
determine if main or pi
"""
hostname = socket.gethostname()
print(hostname)
if hostname in settings.PI_HOST_NAMES:
    IS_PI = True
    # from src.DRL.run_session import train_and_test_bot
    from src.DRL.train import train
elif hostname == settings.PC:
    IS_PI = False
   # from src.main_node.Utils.OverHead import OverHead
    # from src.main_node.Utils.stream_oh_inference import run
else:
    raise Exception("Must configure this device in settings.py")

def main_train_and_test():
    if not IS_PI:
        #oh_stream = OverHead()
        # model = ('ssd_mobilenet_v2_320x320_coco17_tpu-8', 3)
        # run(model, oh_stream)
        threading.Thread(target=subscribe, args=()).start()
        threading.Thread(target=questions.get_user_input, args=()).start()
    else:
        #actions = train_and_test_bot()
        pibot = PiBot2()
        steps = 5
        train.train_session(pibot, steps)
        # publish_data(actions)




if __name__ == "__main__":

    # main()
    main_train_and_test()

    
