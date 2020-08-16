import re

pattern = r"(\w+):(\d+)"
s = "zhang:1994  li:1993"

# 　re 模块调用
l = re.findall(pattern, s)
print(l)

# regex调用
regex = re.compile(pattern)
l = regex.findall(s, pos=0, endpos=13)
print(l)

# 分割字符串

l = re.split(r"\s+", "hello   world")
print(l)

s = re.subn(r'垃圾','**',"玩的真垃圾，张三垃圾",1)
print(s)











