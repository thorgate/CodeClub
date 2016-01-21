from uuid import uuid4

from django.core.cache import cache


class CachedModelMixin:
    def get_cache_key(self):
        return '{className}-hash-{objectID}'.format(className=type(self).__name__, objectID=self.id)

    def get_cache_hash(self):
        key = self.get_cache_key()
        cached_key_hash = cache.get(key)

        if cached_key_hash:
            key_hash = cached_key_hash
        else:
            key_hash = str(uuid4())
            cache.set(key, key_hash)

        return key_hash, not cached_key_hash

    def clear_cache_hash(self):
        cache.delete(self.get_cache_key())
