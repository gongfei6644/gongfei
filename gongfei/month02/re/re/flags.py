import re

#　只匹配ａｓｃｉｉ字符
# regex = re.compile(r'\w+',flags=re.A)

#　匹配时忽略大小写
# regex = re.compile(r"[a-z]\w*",flags = re.I)

#　使 . 可以匹配换行
# regex = re.compile(r'.+',flags = re.S)

#　使^ $匹配每一行开头结尾
regex = re.compile(r"to $",flags=re.M)

s = '''Welcome to 
北京
'''
l = regex.findall(s)
print(l)