import redis
r = redis.Redis(host='localhost', port=6379, db=0)
# r.set(1, 'a')
r.set(2, '中文')
print(r.get(2).decode('utf-8'))
