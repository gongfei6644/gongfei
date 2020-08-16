import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
url = 'http://tieba.baidu.com/p/6169747912'

html = requests.get(url,headers=headers).text
parse_html = etree.HTML(html)
r = parse_html.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')
print(r)











