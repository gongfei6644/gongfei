import requests
import json

class DoubanSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.url = 'https://movie.douban.com/j/' \
                   'chart/top_list?'


    def get_page(self,params):
        res = requests.get(
            url=self.url,
            params=params,
            headers=self.headers,
            verify=False
        )
        # html: '[{},{},{}]'
        html = res.text
        # html:[{},{}]
        html = json.loads(html)
        self.parse_page(html)

    # 解析+保存
    def parse_page(self,html):
        # html: [{},{},{},{}]
        for film in html:
            # 名称
            name = film['title']
            # 评分
            score = film['score']

            print({'name':name,'score':score})


    def main(self):
        menu = '''\033[31m1.剧情
2.喜剧
3.动作
请选择(1/2/3):\033[0m'''
        c = input(menu)
        ty_dict = {'1':'11','2':'24','3':'5'}

        n = input('请输入电影数量:')
        # 定义查询参数
        params = {
            'type': ty_dict[c],
            'interval_id': '100:90',
            'action': '',
            'start': '0',
            'limit': n
        }
        self.get_page(params)

if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main()
















