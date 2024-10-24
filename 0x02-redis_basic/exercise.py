#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Any


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        '''Method that takes a data argument and returns a string'''
        key = str(uuid.uuid4())
        self.__redis.set(key, data)
        return key
