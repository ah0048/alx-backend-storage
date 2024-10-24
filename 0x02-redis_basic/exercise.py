#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Any, Union, Optional, Callable


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        '''Method that takes a data argument and returns a string'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        '''a get method that take a key string argument and a Callable.'''
        value = self._redis.get(key)
        if not value:
            return None
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, key):
        '''Method that takes a value and returns a string'''
        value = self._redis.get(key)
        if not value:
            return None
        return value.decode('utf-8')

    def get_int(self, key):
        '''Method that takes a value and returns an integer'''
        value = self._redis.get(key)
        if not value:
            return None
        return int(value)
