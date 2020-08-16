import re

f = open('test')
data = f.read()

#　大写字母开头单词
# regex = re.compile(r'\b[A-Z]\w*\b')

#　匹配数字
# regex = re.compile(r'\s(-?\d+\.?/?\d*%?)')

#　替换日期
regex = re.compile(r"\d{4}-\d{1,2}-\d{1,2}")

for i in regex.finditer(data):
    # print(i.group())
    print(re.sub(r'-','.',i.group()))


# l = regex.findall(data)
# print(l)
