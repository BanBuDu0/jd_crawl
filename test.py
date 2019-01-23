from db_control import finddata, showall

name = '电脑'
s = showall(name)
if s :
    print(s)
else:
    print("no")