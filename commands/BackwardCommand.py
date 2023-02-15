import commands.CommandInterface as CommandInterface
import controllers.ControllerResolver as ControllerResolver


class BackwardCommand(CommandInterface.CommandInterface):
    def __init__(self):
        self.controller = ControllerResolver.ControllerResolver()

    def execute(self, payload: dict) -> None:
        speed: int = int(payload['speed'])
        distance: int = payload['distance'] if 'distance' in payload else None
        duration: int = payload['duration'] if 'duration' in payload else None

        self.controller.resolve().backward(speed, distance, duration)

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'BACKWARD'
