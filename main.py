#from src.OverHead import OverHead
#from src.ObjectDetection.training import inference
#from src.DRL.Simulator import TestRandomPolicy
#from src.DRL.Environment import SimplifiedRoboEnv, EvenSimplerRoboEnv
from Pi.PiBot.PiBot import PiBot

if __name__ == "__main__":
    #env = EvenSimplerRoboEnv()
    #TestRandomPolicy(env)
   # OH = OverHead()
   # OH.test_cam()
    #inference.inference_test()
    bot = PiBot()
    bot.testing = True
    bot.run()
    
