from utils.Redis import redis


class _AngleService:
    MIN_ANGLE: int = -45
    INIT_ANGLE: int = 0
    MAX_ANGLE: int = 45

    def __init__(self) -> None:
        if not redis.exists('currentAngle'):
            self.setAngle(self.INIT_ANGLE)

    def getCurrentAngle(self, withCast: bool = False) -> int:
        angle: int = int(redis.get('currentAngle').decode('utf-8'))

        if withCast:
            angle += 90

        return angle

    def getMinAngle(self) -> int:
        return self.MIN_ANGLE

    def getInitAngle(self) -> int:
        return self.INIT_ANGLE

    def getMaxAngle(self) -> int:
        return self.MAX_ANGLE

    def setAngle(self, angle: int) -> None:
        if angle < self.MIN_ANGLE:
            redis.set('currentAngle', self.MIN_ANGLE)
        elif angle > self.MAX_ANGLE:
            redis.set('currentAngle', self.MAX_ANGLE)
        else:
            redis.set('currentAngle', angle)


angleService: _AngleService = _AngleService()
