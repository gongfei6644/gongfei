from selenium import webdriver
import time

# 创建浏览器对象
# browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
# 打开百度
browser.get('http://www.baidu.com/')
# 找到搜索框,发送文本
text = browser.find_element_by_xpath(
                             '//*[@id="kw"]')
text.send_keys('赵丽颖')
time.sleep(3)
# 找到 百度一下 按钮,点击
button = browser.find_element_by_xpath(
                            '//*[@id="su"]')
button.click()
# 截图













