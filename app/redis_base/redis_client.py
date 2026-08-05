import redis
import traceback
from app.log.logger import logger
from app.config.config import settings
redis_client=redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

def check_redis_connection() -> bool:
    try:
        return bool(redis_client.ping())
    except redis.RedisError:
        logger.exception(f"traceback:{traceback.format_exc()}")
        return False    