from src.OverHead import OverHead
from src.ObjectDetection.training import inference
from src.DRL.Simulator import TestRandomPolicy
from src.DRL.Environment import SimplifiedRoboEnv
from Pi.PiBot.Actions import Actions

if __name__ == "__main__":
    env = SimplifiedRoboEnv()
    TestRandomPolicy(env)
    OH = OverHead()
    OH.test_cam()
    #inference.inference_test()
    bot = Actions()
    bot.test()
    