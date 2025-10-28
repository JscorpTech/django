# type: ignore
from config.env import env

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env.str("REDIS_HOST", "redis"), env.int("REDIS_PORT", 6379))],
        },
    },
}

