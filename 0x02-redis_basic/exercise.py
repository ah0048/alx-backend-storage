#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Any, Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Decorator that takes a single method
    Callable argument and returns a Callable
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Decorator that takes a single method
    Callable argument and returns a Callable
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))
        return output
    return wrapper


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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


def replay(method: Callable) -> None:
    '''Display the history of calls of a particular function'''
    r = redis.Redis()
    method_name = method.__qualname__
    count = r.get(method_name).decode('utf-8')
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    print(f"{method_name} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{method_name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")
