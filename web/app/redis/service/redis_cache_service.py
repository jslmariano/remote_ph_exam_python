# Generic
import time
import json
import datetime

# Library
import redis

# Main Model
from app.main.service.singleton_service import SingletonMeta

class RedisCache(metaclass=SingletonMeta):
    """docstring for RedisCache"""

    def __init__(self, host="redis", port=6379):
        """
        Constructs a new instance.

        :param      host:        The redis host
        :type       host:        string
        :param      port:        The redis port
        :type       port:        number
        :param      queue_name:  The queue name
        :type       queue_name:  string
        """

        """
        Redis instance connection
        """
        self.r = redis.StrictRedis(host=host, port=port,
                             charset="utf-8", decode_responses=True)

        # Collection of cache keys
        self.cache_keys = dict()

    def save_cache(self, cache_key, _data, _seconds = 5):
        """
        Saves a cache.

        :param      cache_key:   The cache key
        :type       cache_key:   string
        :param      _data:       The data
        :type       _data:       Any

        :returns:   Self instance
        :rtype:     self

        :raises     ValueError:  { exception_description }
        """

        # Enforce data
        if type(_data) != type(dict()):
            raise ValueError("Type of _data is not dict!")

        self.cache_keys[cache_key] = cache_key
        data = json.dumps(_data) #You have to serialize the data to json!
        self.r.setex(
            cache_key,
            _seconds, # Small time for now :)
            # 60*60, # time to store data
            data
        )
        return self

    def has_cache(self, cache_key):
        """
        Determines if cache key exists.

        :param      cache_key:  The cache key
        :type       cache_key:  string

        :returns:   True if cache, False otherwise.
        :rtype:     boolean
        """
        return (cache_key in self.cache_keys.keys())

    def get_cache(self, cache_key):
        """
        Gets the cache.

        :param      cache_key:  The cache key
        :type       cache_key:  string

        :returns:   The cache.
        :rtype:     dict
        """
        _data = self.r.get(cache_key)
        if _data is None:
            return None
        return json.loads(_data)