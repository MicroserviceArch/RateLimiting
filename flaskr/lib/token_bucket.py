import time
from flaskr.lib.redis_config import client as redis_client
from flask import request, Response


def token_bucket_middleware(rate, burst):
    def decorator(app):
        def middleware(*args, **kwargs):
            # Get the IP address of the client
            ip = request.remote_addr

            # Get the current time
            now = time.time()

            # Get the last request time for this IP address
            last = float(redis_client.get(ip) or 0)

            # Calculate the time elapsed since the last request
            elapsed = now - last

            # Calculate the number of tokens to add to the bucket
            increment = elapsed * (rate / 1000)

            # Set the last request time for this IP address
            redis_client.set(ip, now)

            # Get the current number of tokens in the bucket
            tokens = int(float(redis_client.get(ip + '_tokens')) or 0)

            # Calculate the number of tokens in the bucket after this request
            tokens = min(tokens + increment, burst)
            print(tokens)

            # If there are enough tokens in the bucket, allow the request
            if tokens >= 1:
                redis_client.set(ip + '_tokens', tokens - 1)
                return app(*args, **kwargs)

            # Otherwise, return a 429 status (Too Many Requests)
            return Response('Too Many Requests', 429)

        return middleware

    return decorator
