import os, requests
import datetime
from django.core.cache import caches
import os

class CacheBase:
    def __init__(self, ttl=60):
        self.ttl = ttl

    def get(self, key):
        pass

    def set(self, key, value):
        pass


class InAppCache(CacheBase):
    def __init__(self, ttl=10):
        super().__init__(ttl)
        self.cached_data = {}

    def is_expired(self, key):
        if key not in self.cached_data:
            return True
        expire = self.cached_data[key]['datetime']
        return expire is not None and datetime.datetime.now() - datetime.timedelta(seconds=self.ttl) > expire

    def get(self, key):
        print("##---->Trying to get from inapp")
        if key in self.cached_data and not self.is_expired(key):
            print("---->Successful")
            return self.cached_data[key]
        print("---->not Successful")
        return None

    def set(self, key, value):
        self.cached_data[key] = value


class MemcacheLayer(CacheBase):
    def __init__(self, ttl=60):
        super().__init__(ttl)
        self.client = caches["default"]

    def get(self, key):
        print("##---->Trying to get from Memcache")
        data= self.client.get(key)
        if data:
            print("---->Successful")
        else:
            print("---->not Successful")
        return data

    def set(self, key, value):
        self.client.set(key, value, timeout=self.ttl)


class RedisLayer(CacheBase):
    def __init__(self, ttl=300):
        super().__init__(ttl)
        self.client = caches["redis"]

    def get(self, key):
        print("##---->Trying to get from Redis")
        data = self.client.get(key)
        if data:
            print("---->Successful")
        else:
            print("---->not Successful")
        return self.client.get(key)

    def set(self, key, value):
        self.client.set(key, value, self.ttl)






class CacheManager:
    def __init__(self, layers, fetch_func):
        self.layers = layers
        self.fetch_func = fetch_func

    def get(self, key):
        found_value = None
        found_index = None

        for i, layer in enumerate(self.layers):
            print(layer)
            value = layer.get(key)
            if value is not None:
                found_value = value
                found_index = i
                break

        if found_value is None:
            response, content_type = self.fetch_func(key)
            self.set_for_all(key, {'response': response, 'datetime': datetime.datetime.now(), 'content-type': content_type})
            return response, content_type

        for j in range(found_index):
            self.layers[j].set(key, {'response': found_value['response'], 'datetime': datetime.datetime.now(), 'content-type': found_value['content-type']})
        return found_value['response'], found_value['content-type']

    def set_for_all(self, key, value):
        for layer in self.layers:
            layer.set(key, value)

def build_cache_manager(fetch_func):
    order = os.environ.get("CACHE_LAYERS", "inapp,memcache,redis").split(",")
    layers = []
    first_ttl = 10

    for name in order:
        if name == "inapp":
            layers.append(InAppCache(ttl=int(os.environ.get("INAPP_TTL", first_ttl))))
        elif name == "memcache":
            layers.append(MemcacheLayer(ttl=int(os.environ.get("MEMCACHE_TTL", first_ttl))))
        elif name == "redis":
            layers.append(RedisLayer(ttl=int(os.environ.get("REDIS_TTL", first_ttl))))
        first_ttl *= 5

    return CacheManager(layers, fetch_func)

# Sample for fetch_func format 
def fetch_from_api(key):
    print(f"API call for {key}")
    url = os.environ.get("API_URL_TO_CACHE", "https://get.taaghche.com/v2/book/") + str(key)
    print(f"url: {url}")
    response = requests.get(url)
    content_type = response.headers['content-type']
    if response.ok:
        return response, content_type
    return None, None
