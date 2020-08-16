from urllib import request
import csv
import time
import re
import random

class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }
        # 添加计数变量
        self.page = 1

    def get_page(self,url):
        req = request.Request(
            url,
            headers=self.headers
        )
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        # 直接调用解析函数
        self.parse_page(html)

    def parse_page(self,html):
        pattren = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>',re.S)
        film_list = pattren.findall(html)
        # film_list: [('霸王别姬','张国荣','1993'),(),()]
        self.write_csv(film_list)

    # 使用writerow()方法
    # def write_csv(self,film_list):
    #     with open('maoyanfilm.csv','a') as f:
    #         # 初始化写入对象
    #         writer = csv.writer(f)
    #         for film in film_list:
    #             # ('霸王别姬','\n张国荣 ','1993')
    #             L = [
    #                 film[0].strip(),
    #                 film[1].strip(),
    #                 film[2].strip()
    #             ]
    #             writer.writerow(L)
    # 使用writerows()方法
    def write_csv(self,film_list):
        film_last_list = []
        for film in film_list:
            L = ( film[0],film[1].strip(),film[2] )
            film_last_list.append(L)

        with open('maoyanfilm.csv','a') as f:
            # 初始化写入对象
            writer = csv.writer(f)
            writer.writerows(film_last_list)
            # film_last_list : [(),(),()]


    def main(self):
        for offset in range(0,21,10):
            url = self.url.format(str(offset))

            self.get_page(url)
            print('第%d页完成' % self.page)
            self.page += 1
            time.sleep(random.randint(1,3))

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.main()















