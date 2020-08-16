from lxml import etree

# 发请求得到响应内容html
html = '''
<div class="wrapper">
	<i class="iconfont icon-back" id="back"></i>
	<a href="/" id="channel">新浪社会</a>
	<ul id="nav">
		<li><a href="http://domestic.firefox.sina.com/" title="国内">国内</a></li>
		<li><a href="http://world.firefox.sina.com/" title="国际">国际</a></li>
		<li><a href="http://mil.firefox.sina.com/" title="军事">军事</a></li>
		<li><a href="http://photo.firefox.sina.com/" title="图片">图片</a></li>
		<li><a href="http://society.firefox.sina.com/" title="社会">社会</a></li>
		<li><a href="http://ent.firefox.sina.com/" title="娱乐">娱乐</a></li>
		<li><a href="http://tech.firefox.sina.com/" title="科技">科技</a></li>
		<li><a href="http://sports.firefox.sina.com/" title="体育">体育</a></li>
		<li><a href="http://finance.firefox.sina.com/" title="财经">财经</a></li>
		<li><a href="http://auto.firefox.sina.com/" title="汽车">汽车</a></li>
	</ul>
	<i class="iconfont icon-liebiao" id="menu"></i>
</div>
'''
# 创建解析对象
# parse_html = etree.HTML(html)
# # 调用xpath,获取所有a节点的文本内容
# r_list = parse_html.xpath('//a/text()')
# # r_list: ['新浪社会','国内','国际',... ...]
# print(r_list)

# 2、提取所有a节点的href的属性值
parse_html = etree.HTML(html)
r_list = parse_html.xpath('//a/@href')
# print(r_list)

# 3、提取所有href的值,不包括 /
r_list = parse_html.xpath(
    '//ul[@id="nav"]/li/a/@href'
)

# 4、获取 图片、军事、...,不包括新浪社会
r_list = parse_html.xpath(
    '//div[@class="wrapper"]/ul[@id="nav"]/li/a'
    '/text()'
)
for r in r_list:
    print(r)














