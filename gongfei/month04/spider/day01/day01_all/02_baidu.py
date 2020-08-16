from urllib import request

url = 'http://httpbin.org/get'
response = request.urlopen(url)
# 获取内容
html = response.read().decode('utf-8')
print(html)










