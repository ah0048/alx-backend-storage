#!/usr/bin/env python3
'''Python function that lists all documents in a collection'''


def list_all(mongo_collection):
    '''Function that lists all documents in a collection'''
    docs = list(mongo_collection.find())
    if len(docs) == 0:
        return []
    return docs
