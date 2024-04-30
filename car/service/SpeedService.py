from utils.Redis import redis


class _SpeedService:
    MIN_SPEED: int = 0
    INIT_SPEED: int = 60
    MAX_SPEED: int = 100

    def __init__(self) -> None:
        if not redis.exists('currentSpeed'):
            self.setSpeed(self.INIT_SPEED)

    def getCurrentSpeed(self) -> int:
        return int(redis.get('currentSpeed').decode('utf-8'))

    def getMinSpeed(self) -> int:
        return self.MIN_SPEED

    def getInitSpeed(self) -> int:
        return self.INIT_SPEED

    def getMaxSpeed(self) -> int:
        return self.MAX_SPEED

    def setSpeed(self, speed: int) -> None:
        if speed < self.MIN_SPEED:
            redis.set('currentSpeed', self.MIN_SPEED)
        elif speed > self.MAX_SPEED:
            redis.set('currentSpeed', self.MAX_SPEED)
        else:
            redis.set('currentSpeed', speed)


speedService: _SpeedService = _SpeedService()
