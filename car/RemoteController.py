import logging
from car.SpeedService import speedService
from car.BackWheels import BackWheels
from car.CameraMover import CameraMover
from car.FrontWheels import FrontWheels
from car.PCA9685 import PWM
from car.Servo import Servo
from car.TB6612 import Motor
from car.ControllerInterface import ControllerInterface
from utils.Utils import microSleep, singleton


@singleton
class RemoteController(ControllerInterface):
    FRONT_OFFSET: int = -21
    CAMERA_PAN_OFFSET: int = -23
    CAMERA_TILT_OFFSET: int = 18
    BACK_LEFT_OFFSET: int = 0
    BACK_RIGHT_OFFSET: int = 0

    FRONT_PWM_CHANNEL: int = 0
    CAMERA_PAN_PWM_CHANNEL: int = 1
    CAMERA_TILT_PWM_CHANNEL: int = 2
    BACK_LEFT_PWM_CHANNEL: int = 4
    BACK_RIGHT_PWM_CHANNEL: int = 5

    BACK_LEFT_DIRECTION_CHANNEL: int = 17
    BACK_RIGHT_DIRECTION_CHANNEL: int = 27

    def __init__(self, entry: dict) -> None:
        self.entry: dict = entry

        logging.root.setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')

        self.pwm = PWM()

        self.frontWheels = FrontWheels(
            servo=Servo(
                pwm=self.pwm,
                pwmChannel=self.FRONT_PWM_CHANNEL,
                offset=self.FRONT_OFFSET,
            ),
        )

        self.backWheels = BackWheels(
            leftMotor=Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_LEFT_PWM_CHANNEL,
                directionChannel=self.BACK_LEFT_DIRECTION_CHANNEL,
                offset=bool(self.BACK_LEFT_OFFSET),
            ),
            rightMotor=Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_RIGHT_PWM_CHANNEL,
                directionChannel=self.BACK_RIGHT_DIRECTION_CHANNEL,
                offset=bool(self.BACK_RIGHT_OFFSET),
            ),
        )

        self.cameraMover = CameraMover(
            panServo=Servo(
                pwm=self.pwm,
                pwmChannel=self.CAMERA_PAN_PWM_CHANNEL,
                offset=self.CAMERA_PAN_OFFSET,
            ),
            tiltServo=Servo(
                pwm=self.pwm,
                pwmChannel=self.CAMERA_TILT_PWM_CHANNEL,
                offset=self.CAMERA_TILT_OFFSET,
            ),
        )

        self.frontWheels.ready()
        self.backWheels.ready()
        self.cameraMover.ready()
        self.pwm.setup()

    def speed(self, speed: int) -> None:
        speedService.setSpeed(speed)

    def forward(self, speed: int = None) -> None:
        if speed is not None:
            speedService.setSpeed(speed)

        self.backWheels.speed = speedService.getCurrentSpeed()
        self.backWheels.forward()

    def backward(self, speed: int = None) -> None:
        if speed is not None:
            speedService.setSpeed(speed)

        self.backWheels.speed = speedService.getCurrentSpeed()
        self.backWheels.backward()

    def stop(self, duration: float) -> None:
        if duration > 0:
            microSleep(duration)

        self.backWheels.stop()

    def left(self) -> None:
        self.frontWheels.turnLeft()

    def straight(self) -> None:
        self.frontWheels.turnStraight()

    def right(self) -> None:
        self.frontWheels.turnRight()

    def turn(self, angle: int) -> None:
        self.frontWheels.turn(angle)

    def cameraLeft(self) -> None:
        self.cameraMover.turnLeft(40)

    def cameraRight(self) -> None:
        self.cameraMover.turnRight(40)

    def cameraUp(self) -> None:
        self.cameraMover.turnUp(20)

    def cameraDown(self) -> None:
        self.cameraMover.turnDown(20)
