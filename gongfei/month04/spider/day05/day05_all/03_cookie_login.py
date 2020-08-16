import requests
from lxml import etree

url = 'http://www.renren.com/970294164/profile'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "anonymid=jxcu58gtb3su1j; depovince=GW; _r01_=1; JSESSIONID=abcHa63uavQqQcYAbzsUw; ick_login=99eed731-d6e6-435e-86f4-48d79665dc7e; first_login_flag=1; ln_uact=15110225726; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; jebe_key=7bcea0a4-10fd-4ca5-b293-88b450860dbb%7C3317b1face1adcda7e34f17db4558a85%7C1561529179783%7C1%7C1561529181483; jebe_key=7bcea0a4-10fd-4ca5-b293-88b450860dbb%7C3317b1face1adcda7e34f17db4558a85%7C1561529179783%7C1%7C1561529181490; wp_fold=0; td_cookie=18446744069786964649; jebecookies=0c1c850f-7d48-401f-988a-bf559aff0777|||||; _de=5411E55883CC3142BC1347536B8CB062; p=5853eb6bce75b4d8f6f00d71afb004484; t=2e3ba1766211b39caec43c2b1071bd924; societyguester=2e3ba1766211b39caec43c2b1071bd924; id=970294164; xnsid=6d94fc61; loginfrom=syshome",
    "Host": "www.renren.com",
    "Referer": "http://www.renren.com/SysHome.do",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
html = requests.get(url,headers=headers).text
parse_html = etree.HTML(html)
result = parse_html.xpath(
'//*[@id="operate_area"]/div[1]/ul/li[1]/span/text()'
)

print(result)












