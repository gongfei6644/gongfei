# Python爬虫滑块验证
# 滑块验证网址：http://www.cnbaowen.net/api/geetest/

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # 等待元素加载的
from selenium.webdriver.common.action_chains import ActionChains  #拖拽
from selenium.webdriver.support import expected_conditions as EC #等待查找
from selenium.common.exceptions import TimeoutException, NoSuchElementException #错误
from selenium.webdriver.common.by import By #标签查找
from PIL import Image   #处理图片
import requests #处理网络请求
import time
import re #正则
import random #随机数
from io import BytesIO
import os

def merge_image(image_file,location_list):
    """
     拼接图片
    :param image_file:
    :param location_list:
    :return:
    """
    im = Image.open(image_file) #打开图片二进制文件
    im.save('code.jpg') #保存到code.jpg
    new_im = Image.new('RGB',(260,116)) #空白图片长260，宽116的实例
    # 把无序的图片 切成52张小图片
    im_list_upper = []  #上边边
    im_list_down = []   #下半边
    # print(location_list)
    for location in location_list:
        # print(location['y'])
        if location['y'] == -58: # 上半边
            #im.crop(图片的x左坐标，图片的y上坐标，图片的x右坐标，图片的y下坐标)左、上、右和下像素的4元组
            im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,116)))
        if location['y'] == 0:  # 下半边
            #同理如上，返回一个对象的对象PIL.Image.Image的object
            im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))

    x_offset = 0
    for im in im_list_upper: #拼接上半部分
        new_im.paste(im,(x_offset,0))  # 把小图片放到 新的空白图片上，im为无序图片，(x_offset,0)用的是二元组，可以为四元（左上右下），二元或不填，默认为左上方填充
        x_offset += im.size[0] #每一次一定图片的长度

    x_offset = 0    #重置为零，下面同样的拼接下半部分
    for im in im_list_down:
        new_im.paste(im,(x_offset,58))
        x_offset += im.size[0]
    # new_im.show()   #显示生成的图片


    return new_im   #返回这张图片

def get_image(driver,div_path):
    '''
    下载无序的图片  然后进行拼接 获得完整的图片
    :param driver:
    :param div_path:
    :return:
    '''
    time.sleep(2)
    background_images = driver.find_elements_by_xpath(div_path)
    location_list = []
    image_url=""
    for background_image in background_images:
        location = {}
        result = re.findall('background-image: url\("(.*?)"\); background-position: (.*?)px (.*?)px;',background_image.get_attribute('style')) #
        # print(result)
        location['x'] = int(result[0][1])   #获取无序图片x坐标
        location['y'] = int(result[0][2])  #获取无序图片y坐标

        image_url = result[0][0].replace('webp','jpg')     #图片链接
        location_list.append(location)  #将xy坐标 字典放入列表中 {"x":"-157","y":"-58"}


    print('==================================')
        # '替换url http://static.geetest.com/pictures/gt/579066de6/579066de6.webp'
        #content响应的内容，以字节为单位
    image_result = requests.get(image_url).content  #b'\xff\ 字节
    #BytesIO相当于实现一个with open：
    # with open('1.jpg','wb') as f:
    #     f.write(image_result)
    image_file = BytesIO(image_result) # 是一张无序的图片 返回一个对象<_io.BytesIO object at 0x000001B5A139D3B8>

    image = merge_image(image_file,location_list) #拼接图片 <PIL.Image.Image image mode=RGB size=260x116 at 0x1B5A131AD30>

    return image

def get_track(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+(1/2)at²
    ③v²-v0²=2as

    :param distance: 需要移动的距离
    :return: 存放每0.2秒移动的距离
    '''
    # 初速度
    v=0
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t=0.2
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks=[]
    # 当前的位移
    current=0
    accuracy_distance=distance
    # 到达目标值的八分之七，开始减速
    mid=distance * 3/5

    # distance += 20 # 先滑过一点，最后再反着滑动回来
    # a = random.randint(1,3)

    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = random.randint(2,4) # 加速运动的加速度
        else:
            a = -random.randint(2,4) # 减速运动的加速度

        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0*t+0.5*a*(t**2)  #s=v0t+(1/2)at²
        # 当前的位置
        current += s
        # 添加到轨迹列表
        print(a)
        tracks.append(round(s)) #添加每一次x位置的坐标

        # 速度已经达到v,该速度作为下次的初速度
        v= v0+a*t       #记录每一次0.2s的末速度，作为下一个0.2s的初速度，拼接一个滑动动作
    # 反着滑动到大概准确位置
    if abs(current - distance) > 1:
        s = -(current - distance - 1)
        tracks.append(round(s))  # 添加每一次x位置的坐标

    print(current,"<><><>",distance)

    # for i in range(4):
    #    tracks.append(-random.randint(1,3))
    return tracks   #返回位置坐标列表


def get_distance(image1,image2):
    '''
      拿到滑动验证码需要移动的距离
      :param image1:没有缺口的图片对象
      :param image2:带缺口的图片对象
      :return:需要移动的距离
      '''
    # print('size', image1.size)

    threshold = 50 #设置rgb差值
    for i in range(0,image1.size[0]):  # 0到260的x坐标 0
        for j in range(0,image1.size[1]):  # 0到160的y坐标0
            pixel1 = image1.getpixel((i,j)) #返回一个像素值的元组 <class 'tuple'>: (255, 101, 86)
            pixel2 = image2.getpixel((i,j)) #<class 'tuple'>: (255, 101, 86)
            res_R = abs(pixel1[0]-pixel2[0]) # 计算RGB差
            res_G = abs(pixel1[1] - pixel2[1])  # 计算RGB差
            res_B = abs(pixel1[2] - pixel2[2])  # 计算RGB差
            if res_R > threshold and res_G > threshold and res_B > threshold:
                #即判断两张图片的每个像素的色差大于五十，即锁定了缺口，
                #因为滑块起点始终为0，i 的坐标，即为滑块x轴移动距离
                return i  # 需要移动的距离



def main_check_code(driver, element):
    """
     拖动识别验证码
    :param driver:
    :param element:
    :return:
    """
    image1 = get_image(driver, '//div[@class="gt_cut_bg gt_show"]/div') #拼接无序缺口图片1
    image2 = get_image(driver, '//div[@class="gt_cut_fullbg gt_show"]/div') # 拼接无序完整图片2
    # 图片上 缺口的位置的x坐标

    # 2 对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
    l = get_distance(image1, image2) #像素值 182

    print('l=',l)
    # 3 获得移动轨迹
    track_list = get_track(l) #模拟人行为滑动，即匀加速在匀速
    print('第一步,点击滑动按钮')
    #ActionChains执行用户操作的WebDriver实例，按住元素上的鼠标左键。on_element:鼠标向下移动的元素。perform() 执行操作
    ActionChains(driver).click_and_hold(on_element=element).perform()  # 点击鼠标左键，按住不放
    time.sleep(0.3)
    print('第二步,拖动元素')
    for track in track_list:
        #move_by_offset将鼠标移动到当前鼠标位置的偏移量。xoffset为x轴，yoffset为y轴
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
        time.sleep(0.003)
    # if l>100:

    ActionChains(driver).move_by_offset(xoffset=-random.randint(2,5), yoffset=0).perform()
    time.sleep(0.3)
    print('第三步,释放鼠标')
    #释放元素上的已按住的鼠标按钮。 on_element:鼠标向上移动的元素。
    ActionChains(driver).release(on_element=element).perform()

    time.sleep(5)


def main_check_slider(driver):
    """
    检查滑动按钮是否加载
    :param driver:
    :return:
    """
    while True:
        try :
            driver.get('http://www.cnbaowen.net/api/geetest/')
            element = WebDriverWait(driver, 30, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
            if element:
                return element
        except TimeoutException as e:
            print('超时错误，继续')
            time.sleep(5)


if __name__ == '__main__':
    count = 6  # 最多识别6次
    chrome_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")  # 拼接chrome路径
    driver = webdriver.Chrome(executable_path=chrome_path)  # 示列化Chrome
    try:
        # 等待滑动按钮加载完成
        element = main_check_slider(driver) #返回一个 滑块加载的页面
        while count > 0:
            main_check_code(driver,element) #进行滑块验证
            time.sleep(2)
            try:
                success_element = (By.CSS_SELECTOR, '.gt_holder .gt_ajax_tip.gt_success')
                # 得到成功标志
                print('suc=',driver.find_element_by_css_selector('.gt_holder .gt_ajax_tip.gt_success'))
                #等待20s，直到找到成功标签
                success_images = WebDriverWait(driver, 20).until(EC.presence_of_element_located(success_element))
                if success_images: #存在，不为空
                    print('成功识别！！！！！！')
                    count = 0
                    #这里验证完成后就自动跳转，或者再加一个点击跳转，后面跟上你的爬虫数据爬取的自定义函数模块，进行解析即可
                    break
            except NoSuchElementException as e:
                print('识别错误，继续')
                count -= 1
                time.sleep(2)
        else:
            print('too many attempt check code ')
            exit('退出程序')
    finally:
        driver.close()
