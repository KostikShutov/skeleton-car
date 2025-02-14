import cv2
from utils.Utils import singleton


@singleton
class CameraCapturer:
    def __init__(self) -> None:
        self.cap = None
        self.init()

    def init(self) -> None:
        self.cap = cv2.VideoCapture('http://192.168.3.11:8080/?action=stream')

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()

        self.cap = None
