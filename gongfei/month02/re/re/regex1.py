import re

pattern = r'\d+'
s = "2019/4/23,海军70年"

it = re.finditer(pattern, s)
# print(dir(next(it)))
# 　迭代到的内容为ｍａｔｃｈ对象
for i in it:
    print(i.group())  # 获取ｍａｔｃｈ对象内容


#　完全匹配目标字符串内容
obj = re.fullmatch(r"\w+","J_bob")
print(obj.group())

# 匹配目标字符串开始位置
obj = re.match(r"[A-Z]\w+","Hello World")
print(obj.group())

#　匹配目标字符串第一处符合条件内容
obj = re.search(r'\d+',s)
print(obj.group())

