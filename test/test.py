import time
import jieba
import redis
import matplotlib.pyplot as plt
import numpy as np

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
r = redis.Redis(host='localhost', port=6379, db=0)
sentiments = list(str(r.get('sentiments'), encoding='utf-8').split(',')[:-1])
print(len(sentiments))
s = []
for i in sentiments:
    s.append(float(i[0:5]))
    print(float(i[0:4]))
print(len(s))
plt.hist(s, bins=np.arange(0, 1, 0.01))
plt.title("Analysis Sentiments")
plt.xlabel("正面情感概率")
plt.ylabel("数量")
plt.show()
