from src.OverHead import OverHead
from src.ObjectDetection.training import inference
import cv2

def test_cam() -> None:
    # Test overhead camera #
    # VIDEO stream #
    OH = OverHead()
    while True:
        frame = OH.get_frame()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

if __name__ == "__main__":
    # run inference test
    inference.inference_test()
