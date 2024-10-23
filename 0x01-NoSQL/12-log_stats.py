#!/usr/bin/env python3
'''script that provides some stats about Nginx logs stored in MongoDB'''
from pymongo import MongoClient


if __name__ == "__main__":
    '''script that provides some stats about Nginx logs stored in MongoDB'''
    client = MongoClient()
    logs = client.logs.nginx
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    total_num = logs.count_documents({})
    methods_stats = {m: logs.count_documents({"method": m}) for m in method}
    status_check = logs.count_documents({"method": "GET", "path": "/status"})
    print(f"{total_num} logs")
    print("Methods:")
    for m, c in methods_stats.items():
        print(f"\tmethod {m}: {c}")
    print(f"{status_check} status check")
