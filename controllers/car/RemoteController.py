import logging
import controllers.car.AngleService as AngleService
import controllers.car.BackWheels as BackWheels
import controllers.car.SpeedService as SpeedService
import controllers.car.Camera as Camera
import controllers.car.FrontWheels as FrontWheels
import controllers.car.PCA9685 as PCA9685
import controllers.car.Servo as Servo
import controllers.car.TB6612 as TB6612
import controllers.ControllerInterface as ControllerInterface
import commands.CommandPusher as CommandPusher


class RemoteController(ControllerInterface.ControllerInterface):
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

    def __init__(self) -> None:
        logging.root.setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')

        self.angleService = AngleService.AngleService()
        self.speedService = SpeedService.SpeedService()
        self.pwm = PCA9685.PWM()

        self.frontWheels = FrontWheels.FrontWheels(
            angleService=self.angleService,
            servo=Servo.Servo(
                pwm=self.pwm,
                pwmChannel=self.FRONT_PWM_CHANNEL,
                offset=self.FRONT_OFFSET,
            ),
        )

        self.backWheels = BackWheels.BackWheels(
            speedService=self.speedService,
            leftMotor=TB6612.Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_LEFT_PWM_CHANNEL,
                directionChannel=self.BACK_LEFT_DIRECTION_CHANNEL,
                offset=bool(self.BACK_LEFT_OFFSET),
            ),
            rightMotor=TB6612.Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_RIGHT_PWM_CHANNEL,
                directionChannel=self.BACK_RIGHT_DIRECTION_CHANNEL,
                offset=bool(self.BACK_RIGHT_OFFSET),
            ),
        )

        self.camera = Camera.Camera(
            panServo=Servo.Servo(
                pwm=self.pwm,
                pwmChannel=self.CAMERA_PAN_PWM_CHANNEL,
                offset=self.CAMERA_PAN_OFFSET,
            ),
            tiltServo=Servo.Servo(
                pwm=self.pwm,
                pwmChannel=self.CAMERA_TILT_PWM_CHANNEL,
                offset=self.CAMERA_TILT_OFFSET,
            ),
        )

        self.commandPusher = CommandPusher.CommandPusher()

        self.frontWheels.ready()
        self.backWheels.ready()
        self.camera.ready()
        self.pwm.setup()

    def init(self):
        self.angleService.setAngle(90)
        self.speedService.setSpeed(60)

        return {
            'minAngle': self.angleService.getMinAngle(),
            'maxAngle': self.angleService.getMaxAngle(),
            'currentAngle': self.angleService.getCurrentAngle(),
            'minSpeed': self.speedService.getMinSpeed(),
            'maxSpeed': self.speedService.getMaxSpeed(),
            'currentSpeed': self.speedService.getCurrentSpeed()
        }

    def pushCommand(self, payload: object) -> None:
        self.commandPusher.pushCommand(payload)

    def forward(self, speed: int, distance: int = None, duration: int = None) -> None:
        self.speedService.setSpeed(speed)
        self.backWheels.speed = self.speedService.getCurrentSpeed()
        self.backWheels.forward()

    def backward(self, speed: int, distance: int = None, duration: int = None) -> None:
        self.speedService.setSpeed(speed)
        self.backWheels.speed = self.speedService.getCurrentSpeed()
        self.backWheels.backward()

    def stop(self) -> None:
        self.backWheels.stop()

    def left(self) -> None:
        self.frontWheels.turnLeft()

    def straight(self) -> None:
        self.frontWheels.turnStraight()

    def right(self) -> None:
        self.frontWheels.turnRight()

    def turn(self, angle) -> None:
        self.frontWheels.turn(angle)

    def angle(self) -> int:
        return self.angleService.getCurrentAngle()

    def cameraLeft(self) -> None:
        self.camera.turnLeft(40)

    def cameraRight(self) -> None:
        self.camera.turnRight(40)

    def cameraUp(self) -> None:
        self.camera.turnUp(20)

    def cameraDown(self) -> None:
        self.camera.turnDown(20)
