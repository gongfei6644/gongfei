from selenium import webdriver
import time

class JdSpider(object):
    def __init__(self):
        self.url = 'https://www.jd.com/'
        # 创建浏览器对象
        self.browser = webdriver.PhantomJS()
        self.i = 0

    # 打开京东,输入搜索内容,点击搜索
    def get_page(self):
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//*[@id="key"]')\
                                .send_keys('爬虫书籍')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        time.sleep(2)

    # 提取商品信息
    def parse_page(self):
        # 执行js脚本,把进度条拉到最底部
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        # 给留出时间加载网页新的商品
        time.sleep(3)

        li_list = self.browser.find_elements_by_xpath(
                      '//*[@id="J_goodsList"]/ul/li')
        # li_list : [li节点1,li节点2,... ...,li节点30]
        for li in li_list:
            product_list = li.text.split('\n')
            if product_list[0] == '单件':
                # 价格
                price = product_list[2]
                # 名字
                name = product_list[3]
                # 评论
                comment = product_list[4]
                # 商家
                market = product_list[5]
            else:

                # 价格
                price = product_list[0]
                # 名字
                name = product_list[1]
                # 评论
                comment = product_list[2]
                # 商家
                market = product_list[3]
            print([price,market,comment,name])
            self.i += 1

        print(self.i)

    def main(self):
        self.get_page()
        while True:
            self.parse_page()
            # 判断是否应该点击下一页
            if self.browser.page_source.find('pn-next disabled') == -1:
                self.browser.find_element_by_class_name('pn-next').click()
                time.sleep(2)
            else:
                break


if __name__ == '__main__':
    spider = JdSpider()
    spider.main()










