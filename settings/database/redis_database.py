import redis

from settings.settings import REDIS_HOST, REDIS_PORT

redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
