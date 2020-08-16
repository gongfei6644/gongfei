import requests
from lxml import etree

# 1.先POST（把用户名和密码post到一个地址中）
post_url = 'http://www.renren.com/PLogin.do'
post_data = {
    'email' : '15110225726',
    'password' : 'zhanshen001'
}
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer':'http://www.renren.com/SysHome.do'
}
# 实例化session对象
session = requests.session()
session.post(
    url=post_url,
    data=post_data,
    headers = headers
)
# 2.再get（访问需要登录后才能访问的页面）
url = 'http://www.renren.com/970294164/profile'
html = session.get(url,headers=headers).text

parse_html = etree.HTML(html)
result = parse_html.xpath(
'//*[@id="operate_area"]/div[1]/ul/li[1]/span/text()'
)
print(result)














