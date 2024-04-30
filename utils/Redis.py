import redis
from utils.Env import env

host: str = env['REDIS_HOST']
port: int = env['REDIS_PORT']
redis = redis.Redis(host=host, port=port)
