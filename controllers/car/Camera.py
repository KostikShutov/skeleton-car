import logging
from . import Servo


class Camera(object):
    READY_PAN = 90  # Ready position angle
    READY_TILT = 90  # Ready position angle
    CALI_PAN = 90  # Calibration position angle
    CALI_TILT = 90  # Calibration position angle

    CAMERA_DELAY = 0.005
    PAN_STEP = 15  # Pan step = 5 degree
    TILT_STEP = 10  # Tilt step = 5 degree

    def __init__(self,
                 panServo: Servo,
                 tiltServo: Servo) -> None:
        self.panServo = panServo
        self.tiltServo = tiltServo

        self.currentPan = self.READY_PAN
        self.currentTilt = self.READY_TILT

        logging.info('[Camera] Pan servo PWM channel: %d', self.panServo.pwmChannel)
        logging.info('[Camera] Pan servo offset: %d', self.panServo.offset)
        logging.info('[Camera] Tilt servo PWM channel: %d', self.tiltServo.pwmChannel)
        logging.info('[Camera] Tilt servo offset: %d', self.tiltServo.offset)

    def safePlus(self, variable: int, plusValue: int) -> int:
        variable += plusValue
        if variable > 180:
            variable = 180
        if variable < 0:
            variable = 0
        return variable

    def turnLeft(self, step: int = PAN_STEP) -> None:
        self.currentPan = self.safePlus(self.currentPan, step)
        self.panServo.write(self.currentPan)
        logging.info('[Camera] Turn left at step: %d', step)

    def turnRight(self, step: int = PAN_STEP) -> None:
        self.currentPan = self.safePlus(self.currentPan, -step)
        self.panServo.write(self.currentPan)
        logging.info('[Camera] Turn right at step: %d', step)

    def turnUp(self, step: int = TILT_STEP) -> None:
        self.currentTilt = self.safePlus(self.currentTilt, step)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn up at step: %d', step)

    def turnDown(self, step: int = TILT_STEP) -> None:
        self.currentTilt = self.safePlus(self.currentTilt, -step)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn down at step: %d', step)

    def ready(self) -> None:
        self.currentPan = self.READY_PAN
        self.currentTilt = self.READY_TILT
        self.panServo.write(self.currentPan)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn to ready position')
