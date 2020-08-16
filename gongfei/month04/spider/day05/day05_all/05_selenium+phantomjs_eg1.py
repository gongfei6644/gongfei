# 导入selenium中webdriver接口
from selenium import webdriver

# 1.创建浏览器对象
browser = webdriver.PhantomJS()
# 2.输入网址
browser.get('http://www.baidu.com/')
# 获取截图
browser.save_screenshot('baidu.png')
# 打印响应内容
print(browser.page_source.find('su'))

# 关闭浏览器
browser.quit()









