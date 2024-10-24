#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Union


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, float, bytes, int]) -> str:
        '''Method that takes a data argument and returns a string'''
        key = str(uuid.uuid4())
        self.__redis.set(key, data)
        return key
