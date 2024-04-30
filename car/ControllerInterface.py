class ControllerInterface:
    def speed(self, speed: int) -> None:
        pass

    def forward(self, speed: int = None) -> None:
        pass

    def backward(self, speed: int = None) -> None:
        pass

    def stop(self, duration: float) -> None:
        pass

    def left(self) -> None:
        pass

    def straight(self) -> None:
        pass

    def right(self) -> None:
        pass

    def turn(self, angle: int) -> None:
        pass

    def cameraLeft(self) -> None:
        pass

    def cameraRight(self) -> None:
        pass

    def cameraUp(self) -> None:
        pass

    def cameraDown(self) -> None:
        pass
