import redis
import jieba_fast as jieba
r = redis.Redis(host='localhost', port=6379, db=0)
s = r.get('gtx10504055764').decode('utf-8')
s_res = ""
s_cut = jieba.cut(s)
for j in s_cut:
    if j == '不' or j == '非常' or j == '很' or j == '不太':
        s_res += j
    else:
        s_res += j + " "
print(s_res)
