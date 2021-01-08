# import the necessary packages
from threading import Thread
import cv2
class VideoStream:
    """
    threaded stream for camera
    """
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class OverHead:
    def __init__(self, url: str = 'http://192.168.2.163:8080/video') -> None:
        # create a *threaded* video stream, allow the camera sensor to warmup,
        self.stream = VideoStream(url).start()

    def get_frame(self):
        """
        get current frame of video stream
        :return: frame
        """
        frame = self.stream.read()
        return frame

    def __del__(self) -> None:
        """
        clear stream
        :return:
        """
        cv2.destroyAllWindows()
        self.stream.stop()
