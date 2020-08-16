import requests
import json

class TencentSpider(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1559294378106&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1559&postId={}&language=zh-cn'

    # 因为两级页面都需要发请求,写一个发请求的函数
    def get_page(self,url):
        res = requests.get(url,headers=self.headers)
        # 直接把响应转为python数据类型(大字典)
        html = json.loads(res.text)

        return html

    # 解析一级页面
    def parse_one_page(self,html):
        for job in html['Data']['Posts']:
            # job: {1个职位具体信息}
            # 职位名字
            job_name = job['RecruitPostName']
            # postId
            post_id = job['PostId']
            # 拼接二级页面url地址
            two_level = self.two_url.format(post_id)
            # 职责和要求
            job_duty,job_requirement = self.parse_two_page(two_level)

            d = {
                '名称' : job_name,
                '职责' : job_duty,
                '要求' : job_requirement
            }
            print(d)

    def parse_two_page(self,two_level):
        html = self.get_page(two_level)
        # 职责
        job_duty = html['Data']['Responsibility']
        # 要求
        job_requirement = html['Data']['Requirement']

        return job_duty,job_requirement

    def main(self):
        for pageindex in range(1,11):
            url = self.one_url.format(str(pageindex))
            html = self.get_page(url)
            self.parse_one_page(html)

if __name__ == '__main__':
    spider = TencentSpider()
    spider.main()







