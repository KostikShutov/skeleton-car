class StubAutoAlgorithm:
    def execute(self) -> list[dict]:
        return [{
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        }]
