import redis
r = redis.Redis(host='localhost', port=6379, db=0)
for i in r.keys():
    print(i.decode('utf-8'))
print(r.get('gtx10504055764').decode('utf-8'))
