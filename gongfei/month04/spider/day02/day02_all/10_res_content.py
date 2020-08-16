import requests

url = 'http://inews.gtimg.com/newsapp_bt/0/9284458773/1000'
headers = {
    'User-Agent' : 'Mozilla/5.0'
}

html = requests.get(url,headers=headers).content

# 非结构化数据保存
with open('赵丽颖.jpg','wb') as f:
    f.write(html)





















