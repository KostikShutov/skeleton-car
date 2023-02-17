from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class LeftCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: object) -> None:
        self.controller.left()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'LEFT'
