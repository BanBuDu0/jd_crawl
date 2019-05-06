import jieba

s = "非常不错"
seg_list = jieba.cut(s)
a = ""
for i in seg_list:
    a += i + " "
print("okde m a")
print(a)