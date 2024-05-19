import hashlib
from django.core.cache import cache

from common.env import env


class Cache:
    def remember(self, func, key: str):
        cache_enabled = env("CACHE_ENABLED")
        key = hashlib.md5(key.encode("utf-8")).hexdigest()
        response = cache.get(key)

        if (response is None) or cache_enabled:
            response = func()
            cache.set(key, response, env("CACHE_TIME"))

        return response
