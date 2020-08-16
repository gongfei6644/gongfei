from urllib import request,parse

# 定义常用变量
headers = {
    'User-Agent' : ''
}
# 拼接URL地址
word = input('请输入要搜索的内容:')
# 对字符串进行编码
query_string = parse.quote(word)
url = 'http://www.baidu.com/s?wd={}'.format(query_string)
# 发请求获取内容
req = request.Request(url,headers=headers)
res = request.urlopen(req)
html = res.read().decode('utf-8')
# 保存到本地
filename = '{}.html'.format(word)
with open(filename,'w') as f:
    f.write(html)
















