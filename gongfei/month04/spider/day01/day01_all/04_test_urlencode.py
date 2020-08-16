'''向百度搜索赵丽颖的结果的第二页发起请求'''
from urllib import request
from urllib import parse

# 获取url（先编码,再拼接）
baseurl = 'http://www.baidu.com/s?'
headers = {'User-Agent' : 'Mozilla/5.0'}
query_string = {
    'wd' : '赵丽颖',
    'pn' : '10'
}
result = parse.urlencode(query_string)
# 拼接url地址
url = baseurl + result

# 1.创建请求对象
req = request.Request(url,headers=headers)
# 2.获取响应对象
res = request.urlopen(req)
# 3.提取响应对象中的内容
html = res.read().decode('utf-8')

print(html)














