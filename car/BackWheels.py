import logging
import car.TB6612 as TB6612
from car.service.SpeedService import speedService


class BackWheels(object):
    def __init__(self,
                 leftMotor: TB6612,
                 rightMotor: TB6612) -> None:
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        logging.info('[Back wheels] Min speed: %s', speedService.getMinSpeed())
        logging.info('[Back wheels] Max speed: %s', speedService.getMaxSpeed())
        logging.info('[Back wheels] Left motor offset: %s', self.leftMotor.offset)
        logging.info('[Back wheels] Right motor offset: %s', self.rightMotor.offset)
        logging.info('[Back wheels] Set left wheel to %d, PWM channel to %d',
                     self.leftMotor.directionChannel, self.leftMotor.pwmChannel)
        logging.info('[Back wheels] Set right wheel to %d, PWM channel to %d',
                     self.rightMotor.directionChannel, self.rightMotor.pwmChannel)

    def forward(self) -> None:
        self.leftMotor.speed = speedService.getCurrentSpeed()
        self.rightMotor.speed = speedService.getCurrentSpeed()
        self.leftMotor.forward()
        self.rightMotor.forward()
        logging.info('[Back wheels] Running forward with speed %s', speedService.getCurrentSpeed())

    def backward(self) -> None:
        self.leftMotor.speed = speedService.getCurrentSpeed()
        self.rightMotor.speed = speedService.getCurrentSpeed()
        self.leftMotor.backward()
        self.rightMotor.backward()
        logging.info('[Back wheels] Running backward with speed %s' % speedService.getCurrentSpeed())

    def stop(self) -> None:
        self.leftMotor.stop()
        self.rightMotor.stop()
        logging.info('[Back wheels] Stop')

    def ready(self) -> None:
        self.stop()
        logging.info('[Back wheels] Turn to ready position')
