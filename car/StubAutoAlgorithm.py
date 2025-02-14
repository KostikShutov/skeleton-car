import time


class StubAutoAlgorithm:
    def __init__(self, entry: dict) -> None:
        self.entry: dict = entry

    def execute(self) -> list[dict]:
        lastTime: float | None = self.entry['lastTime']

        if lastTime is not None and time.time() - lastTime < 1:
            return []

        return [{
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        }]
