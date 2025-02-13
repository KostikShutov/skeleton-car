class StubAutoAlgorithm:
    def __init__(self, entry: dict) -> None:
        self.entry: dict = entry

    def execute(self) -> list[dict]:
        return [{
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        }]
