from executor.CommandCoordinator import CommandCoordinator


class AutoAlgorithm:
    def __init__(self) -> None:
        self.commandCoordinator: CommandCoordinator = CommandCoordinator()

    def execute(self) -> None:
        self.commandCoordinator.pushCommand({
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        })
