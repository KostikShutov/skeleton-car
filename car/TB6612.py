import logging
import RPi.GPIO as GPIO
import car.PCA9685 as PCA9685


class Motor(object):
    def __init__(self,
                 pwm: PCA9685,
                 pwmChannel: int,
                 directionChannel: int,
                 offset: bool = True) -> None:
        self.pwm = pwm
        self.pwmChannel = pwmChannel
        self.directionChannel = directionChannel
        self._offset = offset
        self.forwardOffset = self._offset
        self.backwardOffset = not self.forwardOffset
        self._speed = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.directionChannel, GPIO.OUT)

        logging.info('[Motor] Setup motor direction channel at %s', self.directionChannel)

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        if speed not in range(0, 101):
            raise ValueError('Speed ranges from 0 to 100, not "{0}"'.format(speed))
        logging.info('[Motor] Set speed to %s', speed)
        self._speed = speed
        pulseWide = int(self.pwm.map(self._speed, 0, 100, 0, 4095))
        self.pwm.write(self.pwmChannel, 0, pulseWide)

    def forward(self) -> None:
        GPIO.output(self.directionChannel, self.forwardOffset)
        self.speed = self._speed
        logging.info('[Motor] Moving forward (%s)', str(self.forwardOffset))

    def backward(self) -> None:
        GPIO.output(self.directionChannel, self.backwardOffset)
        self.speed = self._speed
        logging.info('[Motor] Moving backward (%s)', str(self.backwardOffset))

    def stop(self) -> None:
        self.speed = 0
        logging.info('[Motor] Stop')

    @property
    def offset(self) -> bool:
        return self._offset

    @offset.setter
    def offset(self, value: bool) -> None:
        self.forwardOffset = value
        self.backwardOffset = not self.forwardOffset
        logging.info('[Motor] Set offset to %d', self._offset)
