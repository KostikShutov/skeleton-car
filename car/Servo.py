import logging
import car.PCA9685 as PCA9685


class Servo(object):
    MIN_PULSE_WIDTH: int = 600
    MAX_PULSE_WIDTH: int = 2400
    DEFAULT_PULSE_WIDTH: int = 1500

    def __init__(self,
                 pwm: PCA9685,
                 pwmChannel: int,
                 offset: int = 0,
                 ) -> None:
        if pwmChannel < 0 or pwmChannel > 16:
            raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(pwmChannel))

        self.pwm = pwm
        self.pwmChannel = pwmChannel
        self.offset = offset

        self.write(90)

    def mathToAnalog(self, mathAngle: int) -> int:
        """ Calculate 12-bit analog value from giving angle """
        pulseWide = self.pwm.map(mathAngle, 0, 180, self.MIN_PULSE_WIDTH, self.MAX_PULSE_WIDTH)
        analogValue = int(float(pulseWide) / 1000000 * self.pwm.frequency * 4096)
        logging.info('[Servo] Math angle: %d, Analog angle: %d', mathAngle, analogValue)
        return analogValue

    def write(self, angle: int) -> None:
        """ Turn the servo with giving angle. """
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0

        val = self.mathToAnalog(angle)
        val += self.offset
        self.pwm.write(self.pwmChannel, 0, val)
        logging.info('[Servo] Turn angle to %d', angle)
