#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import time
from functools import wraps

def cache_with_expiry(expiry_time):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(url):
            if url in cache and time.time() - cache[url]["timestamp"] < expiry_time:
                cache[url]["count"] += 1
                return cache[url]["content"]
            else:
                content = func(url)
                cache[url] = {
                    "content": content,
                    "count": 1,
                    "timestamp": time.time()
                }
                return content

        return wrapper

    return decorator

@cache_with_expiry(10)
def get_page(url):
    response = requests.get(url)
    return response.text

# Test the get_page function
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
print(get_page(url))  # This will take 5 seconds to respond
print(get_page(url))  # This will retrieve the cached result

# Wait for 10 seconds
time.sleep(10)

print(get_page(url))  # This will fetch the page again since the cache has expired
