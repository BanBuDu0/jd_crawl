import jieba

s = "我来到清华大学"
seg_list = jieba.cut(s)
a = ""
for i in seg_list:
    a += i + " "
print("okde m a")
print(a)