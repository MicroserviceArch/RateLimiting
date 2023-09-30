import redis

redis_host = 'localhost'  # Your Redis server's host
redis_port = 6379         # Your Redis server's port

client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
