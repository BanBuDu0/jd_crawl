import redis
r = redis.Redis(host='localhost', port=6379, db=0)
# for i in r.keys():
#     print(i.decode('utf-8'))
print(r.get('gtx1050ti3977224').decode('utf-8'))