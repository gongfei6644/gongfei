from selenium import webdriver

browser = webdriver.PhantomJS()
browser.get('https://www.qiushibaike.com/text/')

# 单元素查找
# 1.找到第一个符合条件的就返回
# 2.text属性获取当前节点及后代节点的文本内容
one = browser.find_element_by_class_name('content')
# print(one.text)

# 多元素查找
many = browser.find_elements_by_class_name('content')
for one in many:
    print(one.text)
    print('*'*50)



# '//div[@class="content"]/span'







