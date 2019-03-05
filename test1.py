import time
stra = time.strftime('%Y.%m.%d',time.localtime(time.time()))
s = stra.replace(".", ",")
print(s)