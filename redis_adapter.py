"""TODO"""
from redis import Redis

from env_settings import env_settings


class RedisAdapter:
    """TODO"""
    def __init__(self):
        self._redis = Redis(
            host=env_settings.redis_host,
            port=env_settings.redis_port,
            password=env_settings.redis_password
        )

    def get(self, key):
        """TODO"""
        return self._redis.get(key).decode('utf-8')

    def set(self, key, value):
        """TODO"""
        self._redis.set(key, value)


redis_adapter = RedisAdapter()
