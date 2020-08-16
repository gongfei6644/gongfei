# *Day02回顾**

## **爬取网站思路**

```python
1、找URL规律
2、正则表达式(先分析页面,查看网页源代码)
3、定义程序框架
```

## **存入csv文件**

```python
 import csv
 with open('xxx.csv','w') as f:
 	writer = csv.writer(f)
 	writer.writerow([])
    writer.writerows([(),(),()])
```

## **持久化存储之MySQL**

```mysql
db = pymysql.connect('IP',...)
cursor = db.cursor()
# cursor.execute('SQL',[])
# cursor.execute('SQL',[(),(),()])
db.commit()
cursor.close()
db.close()
```

## **持久化存储之MongoDB**



```python
conn = pymongo.MongoClient('IP',27017)
db = conn['库名']
myset = db['集合名']
# myset.insert_one({})
# myset.insert_many([{},{},{}])
```

## **requests模块**

- get()

```python
 1、发请求并获取响应对象
 2、res = requests.get(url,headers=headers)
```

- 响应对象res属性

```python
res.text ：字符串
res.content ：bytes
res.encoding：字符编码 res.encoding='utf-8'
res.status_code ：HTTP响应码
res.url ：实际数据URL地址
```

## **多级页面数据抓取**

```python
 1、先爬去一级页面,提取链接,继续跟进
 2、爬取二级页面,提取数据
 3、... ... 
```

## **lxml使用流程**

```python
from lxml import etree

parse_html = etree.HTML(res.text)
r_list = parse_html.xpath('xpath表达式')
```

## **xpath**

- 匹配规则

```python
1、节点对象列表 ： //div[@class="tiger"]
2、字符串列表:    //div[@class="t"]/@href
                 //div[@class="t"]/text()
3、函数 ：//div[contains(@id,"tiger")]//a/@href
```

- xpath高级

```python
1、基准xpath表达式(节点对象列表)
2、for r in [节点对象列表]:
       username = r.xpath('.//')
```

********************************************
# **Day03笔记**

## **lxml解析库**

- 安装

```python
sudo pip3 install lxml
```

- 使用流程

```python
1、导模块
   from lxml import etree
2、创建解析对象
   parse_html = etree.HTML(html)
3、解析对象调用xpath
   r_list = parse_html.xpath('xpath表达式')
```

- 练习

```python
from lxml import etree

html = '''<div class="wrapper">
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
</div>'''
# 创建解析对象
parseHtml = etree.HTML(html)
# 调用xpath返回结束,text()为文本内容
rList = parseHtml.xpath('//a/text()')
#print(rList)

# 提取所有的href的属性值
r2 = parseHtml.xpath('//a/@href')
#print(r2)

# 提取所有href的值,不包括 / 
r3 = parseHtml.xpath('//ul[@id="nav"]/li/a/@href')
#print(r3)

# 获取 图片、军事、...,不包括新浪社会
r4 = parseHtml.xpath('//ul[@id="nav"]/li/a/text()')
for r in r4:
    print(r)
```

## **猫眼电影（xpath）**

- 目标

```python
 1、地址: 猫眼电影 - 榜单 - top100榜
 2、目标: 电影名称、主演、上映时间
```

- 步骤

```
1、确定是否为静态页面（右键-查看网页源代码，搜索关键字确认）
2、写xpath表达式
3、写程序框架
```

- xpath表达式

```python
1、基准xpath: 匹配所有电影信息的节点对象列表
    //dl[@class="board-wrapper"]/dd
    
2、遍历对象列表，依次获取每个电影信息
   for dd in dd_list:
	   电影名称 ：dd.xpath('./a/@title')[0].strip()
	   电影主演 ：dd.xpath('.//p[@class="star"]/text()')[0].strip()
	   上映时间 ：dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()
```

- 代码实现（修改之前urllib库代码）

```python
1、将urllib库改为requests模块实现
2、改写parse_page()方法
```

```python
import requests
from lxml import etree
import time
import random

class MaoyanSpider(object):
  def __init__(self):
    self.url = 'https://maoyan.com/board/4?offset={}'
    self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    # 添加计数(页数)
    self.page = 1

  # 获取页面
  def get_page(self,url):
    # random.choice一定要写在这里,每次请求都会随机选择
    res = requests.get(url,headers=self.headers)
    res.encoding = 'utf-8'
    html = res.text
    self.parse_page(html)

  # 解析页面
  def parse_page(self,html):
    #　创建解析对象
    parse_html = etree.HTML(html)
    # 基准xpath节点对象列表
    dd_list = parse_html.xpath('//dl[@class="board-wrapper"]/dd')
    # 依次遍历每个节点对象,提取数据
    for dd in dd_list:
      name = dd.xpath('.//p/a/@title')[0].strip()
      star = dd.xpath('.//p[@class="star"]/text()')[0].strip()
      time = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()

      movie_dict = {
        'name':name,
        'star':star,
        'time':time
      }
      print(movie_dict)

  # 主函数
  def main(self):
    for offset in range(0,31,10):
      url = self.url.format(str(offset))
      self.get_page(url)
      print('第%d页完成' % self.page)
      time.sleep(random.randint(1,3))
      self.page += 1

if __name__ == '__main__':
  spider = MaoyanSpider()
  spider.main()
```

## **链家二手房案例（xpath）**

- 实现步骤

**1. 确定是否为静态**

```python
打开二手房页面 -> 查看网页源码 -> 搜索关键字
```

2. **xpath表达式**

```python
1、修改方法: 右键 -> copy xpath -> 测试修改
2、基准xpath表达式(匹配每个房源信息节点列表)
   //*[@id="content"]/div[1]/ul/li
3、依次遍历后每个房源信息xpath表达式
   * 名称: ./div[1]/div[2]/div/a/text()
   * 总价: ./div[1]/div[6]/div[1]/span/text()
   * 单价: ./div[1]/div[6]/div[2]/span/text()
```

3. **代码实现**

```python
import requests
from lxml import etree
import time

class LianjiaSpider(object):
  def __init__(self):
    self.url = 'https://lf.lianjia.com/ershoufang/pg{}/'
    self.headers = {'User-Agent' : 'Mozilla/5.0'}

  def get_page(self,url):
    res = requests.get(url,headers=self.headers)
    res.encoding = 'utf-8'
    html = res.text
    self.parse_page(html)

  def parse_page(self,html):
    parse_html = etree.HTML(html)
    # 基准xpath
    li_list = parse_html.xpath('//*[@id="content"]/div[1]/ul/li')
    print(li_list)
    # 遍历依次匹配每个房源信息
    for li in li_list:
      house_name = li.xpath('./div[1]/div[2]/div/a/text()')[0].strip()
      total_price = li.xpath('./div[1]/div[6]/div[1]/span/text()')[0].strip()
      unit_price = li.xpath('./div[1]/div[6]/div[2]/span/text()')[0].strip()

      house_dict = {
        'house_name' : house_name,
        'total_price' : total_price,
        'unit_price' : unit_price
      }
      print(house_dict)


  def main(self):
    for pg in range(1,2):
      url = self.url.format(str(pg))
      self.get_page(url)
      print('第%d页爬取成功' % pg)
      time.sleep(0.5)

if __name__ == '__main__':
  spider = LianjiaSpider()
  spider.main()
```

## **百度贴吧图片抓取**

- 目标

```python
抓取指定贴吧所有图片
```

- 思路

```python
1、获取贴吧主页URL,下一页,找到不同页的URL规律
2、获取1页中所有帖子URL地址: [帖子链接1,帖子链接2,...]
3、对每个帖子链接发请求,获取图片URL
4、向图片的URL发请求,以wb方式写入本地文件
```

- 实现步骤

1.  **贴吧URL规律**

```python
http://tieba.baidu.com/f?kw=??&pn=50
```

2. **xpath表达式**

```python
1、帖子链接xpath
   //*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a/@href

2、图片链接xpath
   //div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src
    
3、视频链接xpath
   //div[@class="video_src_wrapper"]/embed/@data-video
   # 注意: 此处视频链接前端对响应内容做了处理,需要查看网页源代码来查看，复制HTML代码在线格式化
```

3. **代码实现**

```python
import requests
from urllib import parse
from lxml import etree

class BaiduImgSpider(object):
  def __init__(self):
    self.url = 'http://tieba.baidu.com/f?{}'
    self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}

  # 获取帖子链接
  def get_tlink(self,url):
    html = requests.get(url,headers=self.headers).text
    # 提取帖子链接
    parse_html = etree.HTML(html)
    tlink_list = parse_html.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a/@href')
    # tlink_list: ['/p/23234','/p/9032323']
    for tlink in tlink_list:
      t_url = 'http://tieba.baidu.com' + tlink
      # 提取图片链接并保存
      self.get_imglink(t_url)

  # 获取图片链接
  def get_imglink(self,t_url):
    res = requests.get(t_url,headers=self.headers)
    res.encoding = 'utf-8'
    html = res.text
    # 提取图片链接
    parse_html = etree.HTML(html)
    # 匹配图片和视频的xpath表达式,中间加或 |
    imglink_list = parse_html.xpath('//*[@class="d_post_content j_d_post_content  clearfix"]/img/@src | //div[@class="video_src_wrapper"]/embed/@data-video')

    for imglink in imglink_list:
      self.write_img(imglink)

  # 保存图片
  def write_img(self,imglink):
    res = requests.get(imglink,headers=self.headers)
    # 切取链接的后10位作为文件名
    filename = imglink[-10:]
    with open(filename,'wb') as f:
      f.write(res.content)
      print('%s下载成功' % filename)

  # 指定贴吧名称,起始页和终止页,爬取图片
  def main(self):
    name = input('请输入贴吧名:')
    begin = int(input('请输入起始页:'))
    end = int(input('请输入终止页:'))
    for page in range(begin,end+1):
      # 查询参数编码
      params = {
        'kw' : name,
        'pn' : str( (page-1)*50 )
      }
      params = parse.urlencode(params)
      url = self.url.format(params)
      # 开始获取图片
      self.get_tlink(url)

if __name__ == '__main__':
  spider = BaiduImgSpider()
  spider.main()
```

## **requests.get()参数**

### **查询参数-params**

- 参数类型

```python
字典,字典中键值对作为查询参数
```

- 使用方法

```python
1、res = requests.get(url,params=params,headers=headers)
2、特点: 
   * url为基准的url地址，不包含查询参数
   * 该方法会自动对params字典编码,然后和url拼接
```

- 示例

```python
import requests

baseurl = 'http://tieba.baidu.com/f?'
params = {
  'kw' : '校花吧',
  'pn' : '50'
}
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
# 自动对params进行编码,然后自动和url进行拼接,去发请求
res = requests.get(baseurl,params=params,headers=headers)
res.encoding = 'utf-8'
print(res.text)
```

### **代理参数-proxies**

- 定义

```python
1、定义: 代替你原来的IP地址去对接网络的IP地址。
2、作用: 隐藏自身真实IP,避免被封。
```

- 普通代理

**获取代理IP网站**

```python
西刺代理、快代理、全网代理、代理精灵、... ... 
```

**参数类型**

```python
1、语法结构
   	proxies = {
       	'协议':'协议://IP:端口号'
   	}
2、示例
    proxies = {
    	'http':'http://IP:端口号',
    	'https':'https://IP:端口号'
	}
```

**示例**

1. 使用免费普通代理IP访问测试网站: http://httpbin.org/get

   ```python
   import requests
   
   url = 'http://httpbin.org/get'
   headers = {
       'User-Agent':'Mozilla/5.0'
   }
   # 定义代理,在代理IP网站中查找免费代理IP
   proxies = {
       'http':'http://163.204.244.99:9999',
       'https':'https://163.204.244.99:9999'
   }
   html = requests.get(url,proxies=proxies,headers=headers,timeout=5).text
   print(html)
   ```

2、使用收费普通代理IP访问测试网站: http://httpbin.org/get

```python
1、从代理网站上获取购买的普通代理的api链接
2、从api链接中提取出IP
3、随机选择代理IP访问网站进行数据抓取
```

```python
import requests
import random

# 提取代理IP
def get_ip_list():
  api_url = 'http://dev.kdlapi.com/api/getproxy/?orderid=985907712281258&num=100&protocol=2&method=2&an_an=1&an_ha=1&sep=1'
  res = requests.get(api_url)
  ip_port_list = res.text.split('\r\n')

  return ip_port_list

# 使用代理IP访问网站

url = 'http://httpbin.org/get'
headers = {'User-Agent' : 'Mozilla/5.0'}
ip_port_list = get_ip_list()

while True:
  proxy_ip = random.choice(ip_port_list)
  proxies = {
    'http' : 'http://{}'.format(proxy_ip),
    'https' : 'https://{}'.format(random.choice(proxy_ip))
  }

  try:
    res = requests.get(url=url,proxies=proxies,headers=headers,timeout=3)
    res.encoding = 'utf-8'
    print(res.text)
    break
  except:
    ip_port_list.remove(proxy_ip)
    print(proxy_ip,'被移除')
    continue
```

3. 思考: 建立一个自己的代理IP池，随时更新用来抓取网站数据

```python
import requests
import random
from lxml import etree
from fake_useragent import UserAgent
import time

# 生成随机的User-Agent
def get_random_ua():
    # 创建User-Agent对象
	ua = UserAgent()
    # 随机生成1个User-Agent
	return ua.random

# 请求头
headers = {
    'User-Agent': get_random_ua()
}
url = 'http://httpbin.org/get'

# 从西刺代理网站上获取随机的代理IP
def get_ip_list():
    # 访问西刺代理网站国内高匿代理，找到所有的tr节点对象
    res = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    parse_html = etree.HTML(res.text)
    # 基准xpath，匹配每个代理IP的节点对象列表
    ipobj_list = parse_html.xpath('//tr')
    # 定义空列表，获取网页中所有代理IP地址及端口号
    ip_list = []
    # 从列表中第2个元素开始遍历，因为第1个为: 字段名（国家、IP、... ...）
    for ip in ipjob_list[1:]:
        ip_info = ip.xpath('./td[2]/text()')[0]
        port_info = ip.xpath('./td[3]/text()')[0]
        ip_list.append(
            {
                'http' :'http://' + ip_info + ':' + port_info,
                'https':'https://' + ip_info + ':' + port_info
            }
        )
    # 随机选择一个代理
    proxies = random.choice(ip_list)
    # 返回代理IP及代理池（列表ip_list）
    return ip_list

# 主程序
def main_print():
    # 我的IP代理池
    ip_list = get_ip_list()
    while True:
        try:
            # 设置超时时间，如果代理不能使用则切换下一个
            proxies = random.choice(ip_list)
            res = requests.get(url=url, headers=headers, proxies=proxies,timeout=5)
            res.encoding = 'utf-8'
            print(res.text)
            
        except Exception as e:
            # 此代理IP不能使用，从代理池中移除
            ip_list.remove(proxies)
            print('%s不能用，已经移除' % proxies)
            # 继续循环获取最后1个代理IP
            continue


if __name__ == '__main__':
    main_print()
```

- 私密代理

**语法格式**

```python
1、语法结构
proxies = {
    '协议':'协议://用户名:密码@IP:端口号'
}

2、示例
proxies = {
	'http':'http://用户名:密码@IP:端口号',
    'https':'https://用户名:密码@IP:端口号'
}
```

**示例代码**

```python
import requests
url = 'http://httpbin.org/get'
proxies = {
    'http': 'http://309435365:szayclhp@42.51.205.96:16819',
    'https':'https://309435365:szayclhp@42.51.205.96:16819',
}
headers = {
    'User-Agent' : 'Mozilla/5.0',
}

html = requests.get(url,proxies=proxies,headers=headers,timeout=5).text
print(html)
```
# **今日作业**


**糗事百科（xpath）**

```python
1、URL地址: https://www.qiushibaike.com/text/
2、目标 ：用户昵称、段子内容、好笑数量、评论数量
```

**电影天堂（xpath）**