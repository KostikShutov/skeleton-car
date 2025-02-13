class AutoAlgorithm:
    def __init__(self, entry: dict) -> None:
        self.entry = entry

    def execute(self) -> list[dict]:
        return [{
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        }]
