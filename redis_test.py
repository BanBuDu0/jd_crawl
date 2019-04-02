import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set(1, 'ooo')
print(r.get(1))
