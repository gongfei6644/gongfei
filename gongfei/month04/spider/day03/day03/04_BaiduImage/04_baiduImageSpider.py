import requests
from lxml import etree
import time

class BaiduSpider(object):
    def __init__(self):
        self.url = 'http://tieba.baidu.com/f?'
        self.headers = {
            # 尽量使用IE的User-Agent,响应内容最标准
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }

    # 获取帖子链接
    def get_tlink(self,params):
        # 请求贴吧页面
        html = requests.get(
            self.url,
            params=params,
            headers=self.headers).text
        # 解析
        parse_html = etree.HTML(html)
        t_list = parse_html.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        # t_list:['/p/23232','/p/09890']
        print(t_list)
        for t in t_list:
            # 拼接每个帖子链接
            t_link = 'http://tieba.baidu.com' + t
            # 向帖子链接发请求,获取图片链接,向图片链接发
            # 请求,保存图片到本地
            self.get_ilink(t_link)

    # 提取图片链接,保存图片
    def get_ilink(self,t_link):
        html = requests.get(
            t_link,headers=self.headers).text
        # 提取图片链接
        parse_html = etree.HTML(html)
        # 正则表达式 | ,匹配图片链接　和　视频链接
        i_list =  parse_html.xpath('//div[@class="d_post_content_main d_post_content_firstfloor"]//div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video')
        print(i_list)
        # i_list: ['http://xxx.jpg','http://xx.jpg']
        for i in i_list:
            html = requests.get(i,
                    headers=self.headers).content
            filename = i[-10:]
            with open(filename,'wb') as f:
                f.write(html)
                print('%sOK' % filename)

    # 主函数(params参数)
    def main(self):
        name = input('请输入贴吧名:')
        begin = int(input('起始页:'))
        end = int(input('终止页:'))

        for page in range(begin,end+1):
            # 定义查询参数
            params = {
                'kw' : name,
                'pn' : str((page-1)*50)
            }
            self.get_tlink(params)


if __name__ == '__main__':
    spider = BaiduSpider()
    spider.main()













