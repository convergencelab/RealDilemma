#from src.OverHead import OverHead
#from src.ObjectDetection.training import inference
#from src.DRL.Simulator import TestRandomPolicy
#from src.DRL.Environment import SimplifiedRoboEnv, EvenSimplerRoboEnv
from Pi.PiBot.PiBot2 import PiBot2

if __name__ == "__main__":
    #env = EvenSimplerRoboEnv()
    #TestRandomPolicy(env)
   # OH = OverHead()
   # OH.test_cam()
    #inference.inference_test()
    #bot = PiBot()
    #bot.test_run()
    bot = PiBot2()
    bot._test_ultrasound()
    
