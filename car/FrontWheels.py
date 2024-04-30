import logging
import car.Servo as Servo
from car.service.AngleService import angleService


class FrontWheels(object):
    def __init__(self, servo: Servo) -> None:
        self.servo = servo

        logging.info('[Front wheels] Min angle: %d', angleService.getMinAngle())
        logging.info('[Front wheels] Max angle: %d', angleService.getMaxAngle())
        logging.info('[Front wheels] Servo PWM channel: %d', self.servo.pwmChannel)
        logging.info('[Front wheels] Servo offset: %d', self.servo.offset)

    def turnLeft(self) -> None:
        angleService.setAngle(angleService.getMinAngle())
        self.turn(angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn left')

    def turnStraight(self) -> None:
        angleService.setAngle(angleService.getInitAngle())
        self.turn(angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn straight')

    def turnRight(self) -> None:
        angleService.setAngle(angleService.getMaxAngle())
        self.turn(angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn right')

    def turn(self, angle: int) -> None:
        angleService.setAngle(angle)
        self.servo.write(angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn angle to %d', angleService.getCurrentAngle())

    def ready(self) -> None:
        self.turnStraight()
        logging.info('[Front wheels] Turn to ready position')
