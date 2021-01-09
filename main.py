from src.OverHead import OverHead
from src.ObjectDetection.training import inference
from Pi.PiBot.Actions import Actions

import cv2



if __name__ == "__main__":
    OH = OverHead()
    OH.test_cam()
    inference.inference_test()
    bot = Actions()
    bot.test()
    
