import logging
from car.service.AngleService import angleService
from car.service.SpeedService import speedService
from car.ControllerInterface import ControllerInterface
from utils.Utils import microSleep, singleton


@singleton
class StubController(ControllerInterface):
    def speed(self, speed: int) -> None:
        speedService.setSpeed(speed)
        logging.info('Speed (speed: %s)' % speed)

    def forward(self, speed: int = None) -> None:
        if speed is not None:
            speedService.setSpeed(speed)

        logging.info('Forward (speed: %s)' % speed)

    def backward(self, speed: int = None) -> None:
        if speed is not None:
            speedService.setSpeed(speed)

        logging.info('Backward (speed: %s)' % speed)

    def stop(self, duration: float) -> None:
        if duration > 0:
            microSleep(duration)

        logging.info('Stop')

    def left(self) -> None:
        oldAngle: int = angleService.getCurrentAngle()
        angleService.setAngle(angleService.getMinAngle())
        newAngle: int = angleService.getCurrentAngle()
        logging.info('Left (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def straight(self) -> None:
        oldAngle: int = angleService.getCurrentAngle()
        angleService.setAngle(angleService.getInitAngle())
        newAngle: int = angleService.getCurrentAngle()
        logging.info('Straight (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def right(self) -> None:
        oldAngle: int = angleService.getCurrentAngle()
        angleService.setAngle(angleService.getMaxAngle())
        newAngle: int = angleService.getCurrentAngle()
        logging.info('Right (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def turn(self, angle: int) -> None:
        oldAngle: int = angleService.getCurrentAngle()
        angleService.setAngle(angle)
        newAngle: int = angleService.getCurrentAngle()
        logging.info('Turn (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def cameraLeft(self) -> None:
        logging.info('Camera left')

    def cameraRight(self) -> None:
        logging.info('Camera right')

    def cameraUp(self) -> None:
        logging.info('Camera up')

    def cameraDown(self) -> None:
        logging.info('Camera down')
