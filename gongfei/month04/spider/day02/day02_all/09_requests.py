import requests

url = 'http://www.baidu.com/'
headers = {
    'User-Agent' : 'Mozilla/5.0'
}

res = requests.get(url,headers=headers)
# 显示字符编码
res.encoding = 'utf-8'
# text : 字符串
print(type(res.text))
# content : 字节流
print(type(res.content))
# status_code: HTTP响应码
print(res.status_code)
# url : 返回实际数据的URL地址
print(res.url)













