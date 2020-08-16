import requests
from lxml import etree
import time
import random

class LianjiaSpider(object):
    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        self.headers = {
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }
        # 添加计数变量
        self.page = 1

    def get_page(self,url):
        res = requests.get(
            url,
            headers=self.headers
        )
        res.encoding = 'utf-8'
        html = res.text

        # 直接调用解析函数
        self.parse_page(html)

    # 用xpath数据提取
    def parse_page(self,html):
        parse_html = etree.HTML(html)
        # 基准xpath:[<>,<>,<>]
        li_list = parse_html.xpath('//li[@class="clear LOGCLICKDATA"]')
        print(len(li_list))

        for li in li_list:
            # 名字
            name = li.xpath('.//div[@class="houseInfo"]/a/text()')[0].strip()
            # 总价
            total_price = li.xpath('.//div[@class="totalPrice"]/span[1]/text()')[0].strip()
            # 单价
            unit_price = li.xpath('.//div[@class="unitPrice"]/span[1]/text()')[0].strip()

            house_dict = {
                '名称' : name,
                '总价' : total_price,
                '单价' : unit_price
            }
            print(house_dict)

    def main(self):
        for pg in range(1,2):
            url = self.url.format(str(pg))

            self.get_page(url)
            print('第%d页完成' % self.page)
            self.page += 1
            time.sleep(random.randint(1,3))

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.main()















