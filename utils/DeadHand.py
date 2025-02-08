from utils.Redis import redis


def isDead() -> bool:
    return not redis.exists('iAmAlive')


def iAmAlive() -> None:
    redis.set(name='iAmAlive', value=1, ex=60)
